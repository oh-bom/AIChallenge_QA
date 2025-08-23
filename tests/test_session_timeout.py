import pytest,time,allure
from pages.LoginPage import LoginPage
from pages.MyPage import MyPage

@pytest.mark.order(3)
@pytest.mark.usefixtures("setup","load_test_data")
class TestSessionTimeout:
    
    @allure.feature("Login")
    @allure.story("부하 테스트")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.session
    def test_session_timeout(self):
        login_page=LoginPage(self.driver,self.base_url)
        login_page.open()
        
        alert_msg=login_page.login(self.common["valid_id"],self.common["valid_pw"])
        
        if not alert_msg: #로그인 성공한 경우
            time.sleep(int(self.common["session_timeout"])) #세션 만료 시간만큼 대기, 실제값보다 작은값으로 변경 후 테스트
        
            my_page=MyPage(self.driver,self.base_url)
            my_page.open()
            assert my_page.check_is_mypage(),"세션 만료됨. 로그인 화면으로 리다이렉트" # 마이페이지 접근이 가능하면 True, 불가능하다면 False
        
        else: #로그인 실패한 경우
            assert False,self.LOGIN_FAILED_MSG # false 리턴과 함께 로그인 실패 출력
        
        