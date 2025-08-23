import pytest,allure
from selenium import webdriver
from utils.DataReader import read_json

@pytest.fixture(scope="class")
def setup(request):
    config=read_json("config.json")
    browser=config["browser"]
    device=config["deviceName"]
     
    if browser=="chrome":
        options=webdriver.ChromeOptions()
        if device:
            mobile_emulation={"deviceName":device}
            options.add_experimental_option("mobileEmulation",mobile_emulation)
        driver=webdriver.Chrome(options=options)     
    else:
        raise ValueError("허용되지 않는 브라우저입니다")
    
    request.cls.driver=driver # request.cls: 현재 테스트 클래스
    yield # yield 앞쪽: setup, yield 뒤쪽: teadown
    driver.quit()
    
@pytest.fixture(scope='class')
def load_test_data(request):
    data=read_json("TestData.json")
    config=read_json("config.json")
    
    request.cls.common=data["common"]
    request.cls.scenarios=data["scenarios"]
    request.cls.base_url=config["base_url"]
    
    request.cls.LOGIN_FAILED_MSG="로그인 실패"
    request.cls.MYPAGE_CONNECT_FAILED_MSG="마이페이지 접근 실패"
    request.cls.INVALID_ALERT_MSG="올바르지 않은 에러 메시지"
    
   
def setup_mutli_browser(browser):
    config=read_json("config.json")
    device=config["deviceName"]
    device_profile=config["device_profile"]
    
    window_size=tuple(map(int,device_profile["window_size"].strip("()").split(",")))
    user_agent=device_profile["user_agent"]

    if browser=="chrome":
        options=webdriver.ChromeOptions()
        if device:
            mobile_emulation={"deviceName":device}
            options.add_experimental_option("mobileEmulation",mobile_emulation)
        driver=webdriver.Chrome(options=options)
        
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument(f"--user-agent={user_agent}")
        driver = webdriver.Edge(options=options)
        driver.set_window_size(*window_size)
        
    elif browser=="firefox":
        options=webdriver.FirefoxOptions()
        options.set_preference("general.useragent.override",user_agent)
        driver=webdriver.Firefox(options=options)
        driver.set_window_size(*window_size)
        
    else:
        raise ValueError(f"{browser}는 지원하지 않는 브라우저입니다.")
    
    return driver
   
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    테스트 실패 시 스크린샷을 Allure Report에 자동 첨부
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = getattr(item.cls, "driver", None)  # 클래스 속성에서 driver 가져오기
        if driver:
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"스크린샷 첨부 실패: {e}") 
        
