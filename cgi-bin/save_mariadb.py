import sys
import mariadb

def saveAuthorize(userID, studentID) -> bool:

    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="put_user_here",
            password="put_pw_here",
            host="localhost",
            port=3306,
            database="put_db_here"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}", file=sys.stderr)
        return False;

    # Get Cursor
    cur = conn.cursor()


    # 사용자 아이디와 학번이 일치하는지를 검사한다.
    try:
        cur.execute("SELECT `studentid` FROM `user` WHERE `id`=?", (userID,))
    except mariadb.Error as e: 
        print(f"Error [USER(1)]: {e}", file=sys.stderr)
        return False
    for studentid in cur:
        if studentid[0] != studentID:
            return False


    # 성공된 인증 내용을 저장한다.
    try:
        cur.execute("""
                UPDATE `user` 
                    SET 
                        `issungshin` = 'Y',
                        `generalcategorycount` = 0,
                        `generalcount` = 0
                    WHERE `id` = '""" + userID + "'")
    except mariadb.Error as e: 
        print(f"Error [USER(2)]: {e}", file=sys.stderr)
        return False


    # 자유게시판은 필수 즐겨찾기 게시판이다.
    try:
        cur.execute("""
                UPDATE `generalcategory` 
                    SET `users` = `users` + 1
                    WHERE `id` = 1
                    """)
        cur.execute("""
                INSERT INTO `generalcategorybookmark`
                    VALUES ('""" + userID + """', 1)
                    """)
    except mariadb.Error as e: 
        print(f"Error [GENERALCATEGORY]: {e}", file=sys.stderr)
        return False


    # 변경사항을 저장한다.
    conn.commit()

    conn.close()

    return True
