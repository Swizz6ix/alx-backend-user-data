#!/usr/bin/env python3
"""A module that defines the expiration of a session"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """Sets the expiration on session"""
    def __init__(self) -> None:
        """Overload initialization parameters"""
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create session Id using parent class"""
        session_id = super().create_session(user_id)
        if type(session_id) is str:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
            return session_id
        else:
            return None

    def user_id_for_session_id(self, session_id=None) -> str:
        """Overload this function in parent class"""
        if session_id in self.user_id_by_session_id:
            user_id_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return user_id_dict['user_id']
            if 'created_at' not in user_id_dict:
                return None
            current_time = datetime.now()
            t_span = timedelta(seconds=self.session_duration)
            exp_time = user_id_dict['created_at'] + t_span
            if exp_time < current_time:
                return None
            return user_id_dict['user_id']
