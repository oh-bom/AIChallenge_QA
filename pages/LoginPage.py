from utils.DataReader import read_json
from pages.BasePage import BasePage
from pages.MyPage import MyPage

locators=read_json("locators.json")["loginPage"]

class LoginPage(BasePage):
    Login_URL = "/user-account/login?my_page=1"
    
    def __init__(self,driver,base_url):
        super().__init__(driver,base_url)
        # self.driver=driver
        
    def open(self):
        self.driver.get(self.base_url+self.Login_URL)
        # self.base_url=base_url
        
    def is_logged_in(self):
        try:
            self.wait_element_disappear(locators["ID_INPUT"])   
            return True
        except:
            return False
        
    def login(self,userId,userPw):
        if userId is not None and userPw is not None:
            self.send_value(locators["ID_INPUT"],userId)
            self.send_value(locators["PW_INPUT"],userPw)
            
        self.click(locators["LOGIN_BTN"])
        msg=self.get_alert_msg()
        
        if msg:
            print("로그인 실패 에러 메시지:",msg)
            return msg
        else:
            my_page=MyPage(self.driver,self.base_url)
            my_page.open()
            assert my_page.check_is_mypage(), self.MYPAGE_CONNECT_FAILED_MSG
            return None

