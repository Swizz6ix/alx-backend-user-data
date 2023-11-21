#!/usr/bin/env python3
""" """
from api.v1.auth.auth import Auth
import binascii
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    Defines the class that handle the implementation of basic authenticatonn
    """
    def __init__(self):
        """Initialize class instance"""

    def extract_base64_authorization_header(
        self, authorization_header: str) -> str:
        """
        A method that returns the Base64 part of the
        Authorization header for a Basic Authentication
        after checking the credentials
        """
        if authorization_header:
            if type(authorization_header) is not str:
                return None
            credentials = authorization_header.split(' ')
            if len(credentials) < 2 or credentials[0] != 'Basic':
                return None
            else:
                return credentials[1]
        return None

    def decode_base64_authorization_header(
        self, base64_authorization_header: str) -> str:
        """
        A method that returns the decoded value of a Base64
        string base64_authorization_header
        """
        if base64_authorization_header:
            if type(base64_authorization_header) is not str:
                return None
            try:
                dcode_str = base64.b64decode(
                    base64_authorization_header,
                    validate=True
                )
                return dcode_str.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None
        return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str) -> (str, str):
        """
        A method that that returns the user email and
        password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header:
            if type(decoded_base64_authorization_header) is not str:
                return (None, None)
            arr = decoded_base64_authorization_header.split(':', 1)
            if len(arr) < 2:
                return (None, None)
            else:
                return (arr[0], arr[1])
        return (None, None)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        A method that that returns the User instance based
        on his email and password.
        """
        if user_email and type(user_email) is str:
            try:
                # Get user with his email and validate his password
                user_obj = User.search({'email': user_email})
            except Exception:
                return None
            if len(user_obj) <= 0:
                return None
            if not user_obj[0].is_valid_password(user_pwd):
                return None
            else:
                return user_obj[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """A method that overloads Auth and retrieves the User
        instance for a request
        """
        header = self.authorization_header(request)
        credentials = self.extract_base64_authorization_header(header)
        d_code_auth = self.decode_base64_authorization_header(credentials)
        email, pwd = self.extract_user_credentials(d_code_auth)
        return self.user_object_from_credentials(email, pwd)
