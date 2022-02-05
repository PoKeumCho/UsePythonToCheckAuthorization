#!/home/auth/anaconda3/bin/python

#==================================================================#
# http://sscommu.com:8000/cgi-bin/authorize.py?userid=&studentid=  #
#==================================================================#

import cgi

header = 'Content-Type: text/html; charset=UTF-8\n\n'
url = '/cgi-bin/authorize.py'

errhtml = '''<!DOCTYPE html>    
                <html lang="ko">    
                    <head>    
                        <meta charset="UTF-8">    
                        <meta name="viewport" content="width=device-width, initial-scale=1.0, mimimum-scale=1.0, user-scalable=no" />
                        <title>오류가 발생하였습니다.</title>
                    </head>    
                    <body>    
                        <h3>ERROR</h3> 
                        <b>%s</b><p>
                        <form>
                            <input type="button" value="back" onclick="window.history.back()">
                        </form>
                    </body>    
                </html>'''  


def showError(error_str):
    print(header + errhtml % (error_str))


formhtml = '''<!DOCTYPE html>    
                <html lang="ko">    
                    <head>    
                        <meta charset="UTF-8">    
                        <meta name="viewport" content="width=device-width, initial-scale=1.0, mimimum-scale=1.0, user-scalable=no" />
                        <title>성신 인증</title>
                    </head>    
                    <body>    
                        <h2><b>성신여자대학교 포탈 시스템 로그인을 통한 인증</b></h2> 
                        <h4>해당 정보는 본교 학생임을 확인하기 위해서만 사용되며, 서버에 저장되지 않습니다.</h4>
                        <form action="/cgi-bin/authorize.py" method="post">
                            <input type="hidden" name="userid" value="%s" />
                            <table>
                                <tr>
                                    <th><label for="studentid">ID : </label></th>
                                    <td><input type="text" id="studentid" name="studentid" value="%s" maxlength="8" readonly /></td>
                                </tr>
                                <tr>
                                    <th><label for="pw">PW : </label></th>
                                    <td><input type="password" id="pw" name="pw" /></td>
                                </tr>
                                <tr>
                                    <th colspan="2">%s</th>
                                </tr>
                                <tr>
                                    <th colspan="2"><input type="submit" value="포탈 시스템 로그인을 통한 인증" /></th>
                                </tr>
                            </table>
                        </form>
                    </body>    
                </html>'''  


def showFrom(userid, studentid, error_str):
    print('%s%s' % (header, formhtml % (userid, studentid, error_str)))


reshtml = '''<!DOCTYPE html>    
                <html lang="ko">    
                    <head>    
                        <meta charset="UTF-8">    
                        <meta name="viewport" content="width=device-width, initial-scale=1.0, mimimum-scale=1.0, user-scalable=no" />
                        <title>성신 인증</title>
                    </head>    
                    <body>    
                        <h1>%s</h1> 
                        %s
                    </body>    
                </html>'''  


def doResult(userid, studentid, pw):

    # 나중에 해당 사이트에 맞는 링크 주소로 변경
    successForm = '''<a href="http://sscommu.com">여기를 클릭해주세요.</a>'''

    failForm = '''
                <form>
                    <input type="button" value="back" onclick="window.history.back()">
                </form>'''


    # 성신여자대학교 포탈 시스템 로그인 성공 여부 확인
    from ssAuthorizedCheck_stronger import ssAuthorizedCheck
    result = ssAuthorizedCheck(studentid, pw)
    # 로그인 성공 시
    if result:
        # 데이터 베이스에 해당 내용을 저장한다.
        from save_mariadb import saveAuthorize
        if saveAuthorize(userid, studentid):
            print('%s%s' % (header, reshtml % ('success', successForm)))
        else:
            print('%s%s' % (header, reshtml % ('오류가 발생하였습니다. 다시 시도해주세요.', failForm)))
    # 로그인 실패 시
    else:
        print('%s%s' % (header, reshtml % ('fail', failForm)))



def process():
    form = cgi.FieldStorage()
    valid = True

    #==================================================
    # GET (사용자의 id, 학번 정보를 같이 전송한다.)
    #==================================================

    if 'userid' in form:
        userid = form['userid'].value 
    else:
        valid = False
        userid = ''

    if 'studentid' in form:
        studentid = form['studentid'].value
    else:
        studentid = ''

    #==================================================
    # POST
    #==================================================

    if 'studentid' in form:
        studentid = form['studentid'].value
    else:
        valid = False
        studentid = ''

    if 'pw' in form:
        pw = form['pw'].value
    else:
        valid = False
        pw = ''

    #==================================================


    # 사용자의 id가 전달(GET)되었으며, 아이디와 비밀번호를 모두 입력한 경우
    if valid:
        doResult(userid, studentid, pw)
    else:
        # 사용자의 id가 전달(GET)되었으나, 아이디 또는 비밀번호를 입력하지 않은 경우
        if userid != '':
            showFrom(userid, studentid, userid + '님 아이디와 비밀번호를 입력해주세요.')
        # 사용자의 id가 전달(GET)되지 않은 경우
        else:
            showError('오류가 발생하였습니다. 다시 시도해 주세요.')



if __name__ == '__main__':
    process()
