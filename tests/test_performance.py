import pytest,time,allure
from pages.LoginPage import LoginPage

@pytest.mark.order(3)
@pytest.mark.usefixtures("setup","load_test_data")
class TestPerformance():
    
    @allure.feature("Login")
    @allure.story("세션 타임아웃")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    def test_performance(self):
        login_page=LoginPage(self.driver,self.base_url)
        start_time = time.time()
        login_page.open()
        
        test_accounts = [(f"user{i}", "wrong_pw") for i in range(1, 6)]
        
        for uid, pw in test_accounts:
            login_page.login(uid, pw)
            _ = login_page.get_alert_msg()

        elapsed = time.time() - start_time
        assert elapsed < 10, f"응답이 너무 느립니다. (소요시간 {elapsed}s)"