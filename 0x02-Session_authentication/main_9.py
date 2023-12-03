#!/usr/bin/python3
"""Check response"""

if __name__ == "__main__":
    try:
        from api.v1.auth.session_db_auth import SessionDBAuth
        sbda = SessionDBAuth()
        user_id = "User9"
        session_id = sbda.create_session(user_id)
        if session_id is None:
            print("create_session should return a Session ID if user_id is valid")
            exit(1)
        user_id_r = sbda.user_id_for_session_id(session_id)
        if user_id_r is None:
            print("user_id_for_session_id should return the User Id linked to the Session id")
            exit(1)
        if user_id_r != user_id:
            print("user_id_for_session_id should return the User ID linked to the session id")
            exit(1)

        print("OK", end="")
    except:
        import sys
        print("Error: {}".format(sys.exc_info()))
