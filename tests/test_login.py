import pytest,allure
from pages.LoginPage import LoginPage

@pytest.mark.order(1)
@pytest.mark.usefixtures("setup","load_test_data")
class TestLogin():
    
    @allure.feature("Login")
    @allure.story("정상 로그인")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.normal
    def test_validation(self):
        login_page=LoginPage(self.driver,self.base_url)
        login_page.open()
        
        alert_msg=login_page.login(self.common["valid_id"],self.common["valid_pw"])
              
        assert alert_msg is None, self.LOGIN_FAILED_MSG # true: 알림 메시지가 없는 경우, false: 알림메시지가 존재하는 경우, 로그인 실패
    
    @allure.feature("Login")
    @allure.story("아이디 누락값 검증")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.empty 
    def test_empty_id(self):
        login_page=LoginPage(self.driver,self.base_url)
        login_page.open()
        scenario=self.scenarios["empty_id"]
        
        alert_msg=login_page.login(scenario["id"],scenario["pw"])
        
        assert alert_msg in scenario["expected_error_msg"], self.INVALID_ALERT_MSG 
        # true: 알림 메시지가 예상 알림 메시지와 일치, false: 알림메시지가 예상 알림메시지와 불일치, "올바르지 않은 에러 메시지" 출력
      
    @allure.feature("Login")
    @allure.story("비밀번호 누락값 검증")
    @allure.severity(allure.severity_level.NORMAL)  
    @pytest.mark.empty
    def test_empty_pw(self):
        login_page=LoginPage(self.driver,self.base_url)
        login_page.open()
        scenario=self.scenarios["empty_pw"]
        
        alert_msg=login_page.login(scenario["id"],scenario["pw"])
        
        assert alert_msg in scenario["expected_error_msg"], self.INVALID_ALERT_MSG
  
    @allure.feature("Login")
    @allure.story("아이디 경계값 검증")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.boundary
    def test_boundary_id(self):
        login_page=LoginPage(self.driver,self.base_url)
        login_page.open()
        scenario=self.scenarios["boundary_id"]
        
        for test_id in [scenario["short_id"],scenario["long_id"]]:
            alert_msg=login_page.login(test_id,scenario["pw"])
            assert any([ alert_msg in scenario["expected_error_msg"],alert_msg in self.common["expected_error_msg"]
            ]), self.INVALID_ALERT_MSG
    
    @allure.feature("Login")
    @allure.story("비밀번호 경계값 검증")
    @allure.severity(allure.severity_level.NORMAL)                
    @pytest.mark.boundary
    def test_boundary_pw(self):
        login_page=LoginPage(self.driver,self.base_url)
        login_page.open()
        scenario=self.scenarios["boundary_pw"]
                     
        for test_pw in [scenario["short_pw"],scenario["long_pw"]]:
            print("pw: ",test_pw)
            alert_msg=login_page.login(scenario["id"],test_pw)
            
            assert any([ alert_msg in scenario["expected_error_msg"],alert_msg in self.common["expected_error_msg"]
            ]), self.INVALID_ALERT_MSG
    
    @allure.feature("Login")
    @allure.story("SQL Injection 차단 검증")
    @allure.severity(allure.severity_level.CRITICAL)        
    @pytest.mark.security    
    def test_sql_injection(self):
        login_page=LoginPage(self.driver,self.base_url)
        login_page.open()
        
        scenario=self.scenarios["sql_injection"]
        test_id=scenario["sql_injection_id"]
        test_pw=scenario["sql_injection_pw"]
        
        alert_msg=login_page.login(test_id,test_pw)
    
        assert alert_msg in self.common["expected_error_msg"], self.INVALID_ALERT_MSG
    
    @allure.feature("Login")
    @allure.story("xss 공격 차단 검증")
    @allure.severity(allure.severity_level.CRITICAL)            
    @pytest.mark.security
    def test_xss_attack(self):
        login_page=LoginPage(self.driver,self.base_url)
        login_page.open()
        
        scenario=self.scenarios["xss_attack"]
        test_id=scenario["xss_attack_id"]
        test_pw=scenario["xss_attack_pw"]
        
        alert_msg=login_page.login(test_id,test_pw)
        assert alert_msg in scenario["expected_error_msg"], self.INVALID_ALERT_MSG
        
    @allure.feature("Login")
    @allure.story("비밀번호 연속 오류 제한 검증")
    @allure.severity(allure.severity_level.CRITICAL) 
    @pytest.mark.security   
    def test_invalid_pw(self):
        login_page=LoginPage(self.driver,self.base_url)
        login_page.open()

        valid_id=self.common["invalid_id"]
        scenario=self.scenarios["consecutive_invalid_pw"]
         
        for i,invalid_pw in enumerate(scenario["invalid_pw_list"]):
            alert_msg=login_page.login(valid_id,invalid_pw)
            
            if alert_msg not in scenario["expected_error_msg"]:
                print(f"{i+1}번째 시도, 로그인 제한 도달하지 않음")
            else:
                print(f"{i+1}번째 시도, 로그인 제한에 도달했습니다.")
                assert (i+1)==int(self.common["login_trial_limit"]), "로그인 횟수 제한 불일치"
                # true: 실제로 로그인 제한에 도달하는데 걸린 횟수(i+1)과 login_trial_limit이 일치, false: 불일치, "로그인 횟수 제한 불일치" 출력
    