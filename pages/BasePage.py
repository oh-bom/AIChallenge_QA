from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver,base_url):
        self.driver = driver
        self.base_url=base_url
        self.wait = WebDriverWait(driver, 10)
        self.MYPAGE_CONNECT_FAILED_MSG="마이페이지 접근 실패"
        
    def get_by(self,locator):
        by_map={
            "id":By.ID,
            "xpath":By.XPATH
        }
        
        return by_map[locator["by"]],locator["value"]

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(self.get_by(locator))).click()

    def send_value(self, locator, text):
        self.wait.until(EC.visibility_of_element_located(self.get_by(locator))).clear()
        self.driver.find_element(*self.get_by(locator)).send_keys(text)

    def find_element_by(self,locator):
        return self.driver.find_element(*self.get_by(locator))
    def wait_element_appear(self,locator):
        self.wait.until(EC.visibility_of_element_located(self.get_by(locator)))
    
    def wait_element_disappear(self,locator):
        self.wait.until(EC.invisibility_of_element_located(self.get_by(locator)))
    
    def get_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(self.get_by(locator))).text
    
    def get_alert_msg(self,timeout=5):
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            text=alert.text
            alert.accept()
            return text
        except:
            return None