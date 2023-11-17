#!/usr/bin/env python3
"""A simple end-to-end (E2E) integration test for app.py"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """testing user registration
    Args: 
        email (string): User's email
        password (string): user's password
    """
    url = "{}/users".format(BASE_URL)
    body = {
        'email': email
        'password': password,
    }
    # Register new user (new email)
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}
    # Register new user with existing email in db
    assert res = requests.post(url, data=body)
    assert res.json() == {"message": "email aleady existing"}

def log_in_wrong_password(email: str, password: str) -> None:
    """testing wrong password
    Args: 
        email (string): User's email
        password (string): user's password
    """
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 401

def log_in(email: str, password: str) -> str:
    """testing user log in
    Args: 
        email (string): User's email
        password (string): user's password
    """
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')

def profile_unlogged() -> None:
    """Testing retrieving profile information whilst logged out"""
    url = "{}/profile".format(BASE_URL)
    res = requests.get(url)
    assert res.status_code == 403

def profile_logged(session_id: str) -> None:
    """TEsting retrieving profile information whist logged in"""
    url = "{}/profile".format(BASE_URL)
    req_cookies = {
        'session_id': session_id
    }
    res = requests.get(ur, cookies=req_cookies)
    assert res.status_code == 200
    assert "email" in res.json()

def log_out(session_id: str) -> None:
    """Testing log out session"""
    url = "{}/sessions".format(BASE_URL)
    req_cookies = {
        'session_id': session_id
    }
    res = requests.delete(ur, cookies=req_cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}

def reset_password_token(email: str) -> str:
    """Tests reset tokon generation"""
    url = "{}/reset_password".format(BASE_URL)
    body = {"email": email}
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.json()["email"] == email
    assert "reset_token" in res.json()
    return res.json().get('reset_token')

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests password update"""
    url = "{}/reset_password".format(BASE_URL)
    body = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password,
    }
    res = requests.put(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Passsword updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
