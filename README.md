# AIChallenge_QA - 로그인 기능 자동화 테스트

**알바몬 모바일 웹** 개인회원 로그인 자동화 테스트를 위한 코드입니다.  
Pytest + Selenium WebDriver 기반으로 작성되었으며, Allure Report와 pytest-html을 통해 테스트 결과를 리포트합니다.  

---

## 📌 1. 환경 세팅

```bash
git clone <repo_url>
cd AIChallenge_QA

# 가상환경 생성 및 실행
python -m venv venv
source venv/bin/activate   # (Windows: venv\Scripts\activate)

# 라이브러리 설치
pip install -r requirements.txt
````

---

## 📌 2. 테스트 대상

* **서비스** : [알바몬 모바일 웹](https://m.albamon.com/)
* **기능** : 개인회원 로그인

### 기능 요구사항

* 아이디 + 비밀번호 입력 로그인
* 입력값 유효성 검증 (아이디/비밀번호 누락, 글자수 제한)
* 보안 검증 (SQL Injection, XSS 공격, 다중 로그인, 세션 타임아웃)
* 성능 검증 (응답속도)
* 호환성 검증(모바일 기기별 UI)
* `PASSED / FAILED` 출력, 로그인 실패 시 오류 메시지 출력
* 로그인 성공 시 마이페이지(`/personal/mypage`) 이동

---

## 📌 3. 디렉토리 구조

```bash
project-root/
├── config/                         # 환경 설정 관련 파일
│   ├── config.json                 # 공통 설정
│   ├── devices.json                # 디바이스별 설정
│   ├── locators.json               # UI 요소 locator 정보
│   └── TestData.json               # 테스트 데이터
│
├── pages/                          # Page Object Model (POM) 구조
│   ├── __init__.py
│   ├── BasePage.py                 # 공통 Page 클래스
│   ├── LoginPage.py                # 로그인 페이지 객체
│   └── MyPage.py                   # 마이페이지 객체
│
├── reports/                        # 테스트 결과 리포트
│   ├── allure-results/             # Allure Report 결과
│   └── html-results/               # pytest-html 결과
│
├── screenshots/                    # 실행 중 캡처 이미지 저장
│
├── tests/                          # 테스트 코드 모음
│   ├── __init__.py
│   ├── conftest.py                 # pytest 공통 fixture 정의
│   ├── pytest.ini                  # pytest 설정 파일
│   ├── test_login.py               # 기본 로그인 테스트(아이디/비밀번호 누락, 글자수, SQL Injection, XSS)
│   ├── test_mobile_devices.py      # 모바일 디바이스 UI 테스트
│   ├── test_multisession_login.py  # 다중 세션 로그인 테스트
│   ├── test_performance.py         # 성능 테스트
│   └── test_session_timeout.py     # 세션 타임아웃 테스트
│
└── README.md                       # 프로젝트 설명 문서
```

---

## 📌 4. 실행 방법

### 1) Allure Report 실행

```bash
pytest -v --alluredir=reports/allure-results
allure serve reports/allure-results
```

### 2) HTML Report 실행

```bash
pytest -v --html=reports/html-results/report.html --self-contained-html
```

---

## 📌 5. 테스트 분류

* **기능 테스트**: 정상 로그인, 누락값 검증, 경계값 검증
* **보안 테스트**: SQL Injection, XSS, 다중 로그인, 세션 타임아웃, 연속 로그인 시도 제한
* **성능 테스트**: 다중 계정 응답 속도 측정
* **호환성 테스트**: 다양한 모바일 기기 UI 확인

---

## 📌 6. Pytest 마커 설명

| 마커 이름         | 설명                           |
| ------------- | ---------------------------- |
| `normal`      | 정상 로그인                      |
| `empty`       | 입력값 누락 검증                    |
| `boundary`    | 아이디/비밀번호 경계값 검증              |
| `security`    | 보안 검증 (SQL Injection, XSS 등 ) |
| `session`     | 세션 관련 검증 (다중 로그인, 타임아웃)      |
| `performance` | 응답 속도 체크                 |
| `devices`     | 모바일 기기별 UI 검증                |

---

## 📌 7. 테스트 케이스 요약

테스트 케이스 요약표입니다.

[전체 테스트 케이스](https://docs.google.com/spreadsheets/d/18ps3tgWn5rLZ194R5b0JJucD_s9ccmoYAt57V2cOcPU/edit?usp=sharing)는 링크를 참고해주세요

| Test Scenario   | Test Case             | Priority | Type          | Test Data                          |  Expected Result                               | PASS/FAIL | Class Name                | Function Name                      | Marker Name          |
| ------ | -------------------- | ---- | ----------- | ------------------------------- | ---------------------------------------------------------- | ----- | ----------------------- | -------------------------- | ----------- |
| 정상 로그인 | 유효한 아이디, 유효한 비밀번호 입력 | P1   | Positive    | valid\_id / valid\_pw           | 로그인 성공 후 마이페이지 이동                                          | PASS  | `TestLogin`             | `test_validation`          | normal      |
| 누락값 검증 | 아이디 누락               | P1   | Negative    | "" / valid\_pw                  | "아이디를 입력해주세요." 오류 메시지 출력                                   | PASS  | `TestLogin`             | `test_empty_id`            | empty       |
| 누락값 검증 | 비밀번호 누락              | P1   | Negative    | valid\_id / ""                  | "비밀번호를 입력해주세요." 오류 메시지 출력                                  | PASS  | `TestLogin`             | `test_empty_pw`            | empty       |
| 경계값 검증 | 6자 미만, 16자 초과 아이디    | P1   | Negative    | short/long ID                   | "아이디는 6\~16자여야 합니다." 또는 "아이디 또는 비밀번호가 일치하지 않습니다." 메시지 출력   | PASS  | `TestLogin`             | `test_boundary_id`         | boundary    |
| 경계값 검증 | 8자 미만, 16자 초과 비밀번호   | P1   | Negative    | short/long PW                   | "비밀번호는 8\~16자여야 합니다." 또는 "아이디 또는 비밀번호가 일치하지 않습니다." 메시지 출력  | PASS  | `TestLogin`             | `test_boundary_pw`         | boundary    |
| 보안 검증  | SQL Injection 입력     | P1   | Security    | `' OR '1'='1`                   | "아이디 또는 비밀번호가 올바르지 않습니다." 메시지 출력                           | PASS  | `TestLogin`             | `test_sql_injection`       | security    |
| 보안 검증  | XSS 공격 입력            | P1   | Security    | `<script>alert('XSS')</script>` | "아이디 또는 비밀번호가 올바르지 않습니다." 메시지 출력                           | PASS  | `TestLogin`             | `test_xss_attack`          | security    |
| 보안 검증  | 연속 비밀번호 오류 n회        | P1   | Security    | wrong\_pw\_1\~n                 | "연속된 로그인 실패로 일시적으로 차단되었습니다." 또는 "비밀번호 변경 후 재로그인 필요" 메시지 출력 | PASS  | `TestLogin`             | `test_invalid_pw`          | security    |
| 호환성 검증 | 모바일 기기별 UI           | P2   | Positive    | iPhone / Android                | ID 입력창, PW 입력창, 로그인 버튼이 정상적으로 노출                           | PASS  | `TestMobileDevices`     | `test_login_devices`       | devices     |
| 세션 검증  | 다중 세션 로그인            | P3   | Security    | 동일 계정                           | 두 번째 로그인 시 기존 세션 종료 또는 로그인 차단                              | FAIL  | `TestMultiSessionLogin` | `test_multi_session_login` | session     |
| 세션 검증  | 세션 타임아웃              | P3   | Security    | valid\_id / valid\_pw           | 세션 만료 시 로그인 페이지로 이동 및 재로그인 요구                              | PASS(TBD)   | `TestSessionTimeout`    | `test_session_timeout`     | session     |
| 성능 검증  | 계정 5개 순차 로그인           | P3   | Performance | valid\_id1\~5                   | 전체 로그인 응답 시간 < 10초                                         | FAIL(TBD)   | `TestPerformance`       | `test_performance`         | performance |

---

## 📌 8. 리포트 / 스크린샷 예시

* **Allure Report**
<img width="1616" height="1468" alt="image" src="https://github.com/user-attachments/assets/39b92f39-dd17-4095-935e-dba51f094f22" />


* **HTML Report**
  <img width="2048" height="909" alt="image" src="https://github.com/user-attachments/assets/5adb57ec-54c4-4988-900b-94039c778bcb" />


* **모바일 기기별 UI 캡처**
  `screenshots/` 폴더에 저장됨

---

## 📌 9. 기술 스택

* Python 3.11
* Pytest
* Selenium WebDriver
* Allure Report
* pytest-html

---

## 📌 10. 향후 개선 사항
* 서버에서 정의된 로그인 시도 제한 횟수, 세션 타임아웃 값 등을 적용하여 실제 운영 환경 기준으로 보안/세션 관리 기능 측정
* 회원가입, 아이디 찾기, 비밀번호 찾기 등 검증 범위 확대
* Jenkins/GitHub Actions 기반 CI/CD 적용
* 테스트 커버리지 리포트 추가

---

