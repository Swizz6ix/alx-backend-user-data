#!/usr/bin/env python3
"""A model that that enables session to be stored in database"""
from models.base import Base

class UserSession(Base):
    """A model that allows sessions to be stored in the database"""
    def __init__(self, *args: list, **kwargs: dict):
        """Initializing class instance/object with base class args"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session = kwargs.get('session_id')
