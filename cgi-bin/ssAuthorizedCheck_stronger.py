import sys
import time
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
 
 
def ssAuthorizedCheck(ID, PW):
    """로그인을 통해서 성신여대 학생 여부를 확인한다."""

    # firefox 모듈의 WebDriver 객체를 생성한다.
    driver = webdriver.Firefox()

    # 인증 결과를 저장한다.
    is_ssAuthorized = False
 
    # 로그인 페이지를 엽니다.
    print('Accessing to sign in page ...', file=sys.stderr)
    driver.get('https://portal.sungshin.ac.kr/sso/login.jsp')
 
    # 로그인 페이지에 들어가졌는지 확인한다.
    # title 요소의 텍스트가 일치하지 않으면 AssertionError 예외가 발생한다.
    assert ':: 성신여자대학교 포탈시스템::' in driver.title
 
    driver.find_element_by_id('loginId_pc').send_keys(ID)
    driver.find_element_by_id('loginPwd_pc').send_keys(PW)
    driver.find_elements_by_class_name('login_btn')[1].click()

    # 바로 로드되지 않으므로 약간의 시간 간격을 둔다.    
    time.sleep(2)

    try:
        driver.close()              # 윈도우 창을 닫는다.
                                    # 아이디 또는 비밀번호가 일치하디 않으면 해당 코드를 실행하였을때
                                    # UnexpectedAlertPresentException 예외가 발생한다.
        is_ssAuthorized = True
        print('Authorized', file=sys.stderr)
    except UnexpectedAlertPresentException as e:
        print('not Authorized : ' + str(e), file=sys.stderr)
        driver.close()

    # 인증 결과를 반환한다.
    return is_ssAuthorized
