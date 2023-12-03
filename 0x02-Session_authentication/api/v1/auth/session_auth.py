#!/usr/bin/env python3
"""
describes a new authentication mechanism
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Authentication mechanism using session auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """A method that creates a Session ID for a user_id"""
        if type(user_id) is str:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """A method that returns a User ID based on a Session ID"""
        if session_id:
            if type(session_id) is str:
                return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """A method that returns a User instance based on a cookie value"""
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None): 
        """A method that deletes the user session / logout"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if request is None or session_id is None or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
