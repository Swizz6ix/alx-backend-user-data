#!/usr/bin/env python3
"""
This module handles the user's authenticaton
"""
import bcrypt
from db import DB
from typing import TypeVar, Union
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from user import User

def _hash_password(password: str) -> bytes:
    """
    Hash user's password
    Args:
        password (str): user's password
    Return:
        bytes
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    checks if the provided password matches the hashed_password
    Args:
        password (string): user's original password
        hashed_password (bytes): hashed password
    Return:
        boolean
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def _generate_uuid() -> str:
    """Generate unique id"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register user if it does not exist, hash password and save to database
        return a ValueError if user already exist
        Args:
            email (string): user's email
            password (string): user's password
        Return:
            User Object or ValueError
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        validate user before login
        1. checks if email is registered
        2, checks if password is properly hashed
        Args:
            email (string): user's email
            password (string): user's password
        Return:
            boolean
        """
        try:
            user = self._db.find_user_by(email=email)
            return is_valid(user.hashed_password, password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Creates the sessionId
        Args:
            email (string): user's email
        Return:
            string
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        else:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Getting user using session id instead of email and password
        for re-verification
        Args:
            session_id (string): session id of the user's session
        Return:
            User or None
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return User

    def destroy_session(self, user_id: str) -> None:
        """
        Destroy the session id of a user, when the user logs out
        Args:
            user_id (string): the user id of the user
        Returns:
            None
        """
        if not user_id:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """generates password reset token
        Args:
            email (string): user's email
        Return:
            string
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if not user:
            raise ValueError
        new_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=new_token)
        return new_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user's password
        Args:
            reset_token (str): the generated reset token
            password (str): the new password of the user
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if not user:
            raise ValueError()
        new_password = _hash_password(password)
        self._db.update_user(
            user.id, 
            hashed_password=hashed_password,
            reset_token=None
        )
        return None
