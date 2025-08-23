import pytest,allure
from selenium import webdriver
from utils.DataReader import read_json
from pages.LoginPage import LoginPage

DEVICE_LIST=read_json("devices.json")
config=read_json("config.json")
locators=read_json("locators.json")["loginPage"]


@pytest.mark.order(2)
class TestMobileDevices():
    
    @allure.feature("Login")
    @allure.story("모바일 기기별 UI 검증")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("device_name",DEVICE_LIST) # 테스트 디바이스 리스트를 device_name 파라미터로 전달 
    @pytest.mark.devices
    def test_login_devices(self,device_name):
        options = webdriver.ChromeOptions()
        mobile_emulation = { "deviceName": device_name }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        driver = webdriver.Chrome(options=options)
        
        try:
            login_page=LoginPage(driver,config["base_url"])
            login_page.open()
            
            assert login_page.find_element_by(locators["ID_INPUT"]) is not None, f"[{device_name}] 아이디 입력 필드가 없거나 깨짐" #false: ui요소를 발견하지 못한 경우, 에러 메시지 출력
            assert login_page.find_element_by(locators["PW_INPUT"]) is not None, f"[{device_name}] 비밀번호 입력 필드가 없거나 깨짐"
            assert login_page.find_element_by(locators["LOGIN_BTN"]) is not None, f"[{device_name}] 로그인 버튼이 없거나 깨짐"

            driver.save_screenshot(f"screenshots/login-{device_name}.png") # 화면 캡처 저장

        finally:
            driver.quit()