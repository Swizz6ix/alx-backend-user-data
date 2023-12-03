#!/usr/bin/env python3
"""A mudule that stores authorizaation in database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
from flask import request


class SessionDBAuth(SessionExpAuth):
    """
    stores authorization system in database with expiration time
    """
    def create_session(self, user_id=None):
        """
        A module that creates and stores new instance of UserSession
        and returns the Session ID
        """
        session_id = super().create_session(user_id)
        if type(session_id) is str:
            dic = {
                'user_id': user_id,
                'session_id': session_id
            }
            new_user = UserSession(**dict)
            new_user.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        A module that returns the User ID by requesting UserSession
        in the database based on session_id
        """
        try:
            session_dic = UserSession.search({'session_id', session_id})
        except Exception:
            return None
        """Set expiration time by adding more seconds/minutes to the created
        time from shell env"""
        if len(session_dic) <= 0:
            return None
        current_time = datetime.now()
        t_span = timedelta(seconds=self.session_duration)
        exp_time = session_dic[0].created_at + t_span
        if exp_time < current_time:
            return None
        return session_dic[0].user_id

    def destroy_session(self, request=None):
        """A method that destroys the UserSession based
        on the Session ID from the request cookie"""
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id', session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
