from pages.BasePage import BasePage

class MyPage(BasePage):
    MyPage_URL="/personal/mypage"
    
    def __init_(self,driver,base_url):
        super().__init__(driver,base_url)
        # self.driver=driver
        
    def open(self):
        self.driver.get(self.base_url+self.Login_URL)
        # self.base_url=base_url
        
        
    def open(self):
        self.driver.get(self.base_url+self.MyPage_URL)
        
    def check_is_mypage(self):
        return self.driver.current_url==self.base_url+self.MyPage_URL