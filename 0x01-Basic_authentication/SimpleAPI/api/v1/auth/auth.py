#!/usr/bin/env python3
"""Auth class to manage API authentication"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """Define the class that handles authentication"""
    def __init__(self):
        """initialize class instance"""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """specifies which route/path requires authentication and one that
        does not require authentcation
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        r_path = path.rstrip('/')
        for ex_path in excluded_paths:
            ex_path = ex_path.rstrip('/')
            if fnmatch.fnmatch(r_path, ex_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Handles authentication of credentials in http header"""
        auth = request.headers.get('Authorization') if request is not None \
        else None
        if request is None or auth is None:
            return None
        else:
            return auth

    def current_user(self, request=None) -> TypeVar('User'):
        """return object of class user"""
        return None
