import pytest,allure
from tests.conftest import setup_mutli_browser
from pages.LoginPage import LoginPage

@pytest.mark.order(3)
@pytest.mark.usefixtures("load_test_data")
class TestMultiSessionLogin:
    
    @allure.feature("Login")
    @allure.story("다중 세션 로그인 차단 검증")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.session
    def test_multi_session_login(self):
        chrome_driver=setup_mutli_browser("chrome")
        login_page=LoginPage(chrome_driver,self.base_url)
        login_page.open()
        
        alert_msg=login_page.login(self.common["valid_id"],self.common["valid_pw"])
        assert alert_msg is None, self.LOGIN_FAILED_MSG # alert_msg가 none이면 정상 로그인 상태
            
        firefox_driver=setup_mutli_browser("firefox")
        login_page=LoginPage(firefox_driver,self.base_url)
        login_page.open()
        
        alert_msg=login_page.login(self.common["valid_id"],self.common["valid_pw"])
        assert (alert_msg is not None) and (alert_msg in self.scenarios["multi_session"]["expected_error_msg"]),"다중 세션 로그인 허용"
        # True: aert_msg가 multi_session 에러메시지(다른 브라우저에서 로그인이 되어있습니다.)와 동일하다면 다중 세션 로그인을 허용하지 않음
        # False: 다중세션 로그인을 허용하여 에러 메시지가 발생하지 않음
        
        chrome_driver.quit()
        firefox_driver.quit()