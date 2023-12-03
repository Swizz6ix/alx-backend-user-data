#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
# environment variable
AUTH_TYPE = os.getenv('AUTH_TYPE', 'auth')
if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif AUTH_TYPE == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif AUTH_TYPE == 'session_db_auth':
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_request(error) -> str:
    """Unauthorized request"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def no_access_res(error) -> str:
    """Authenticate but not allow access to resources"""
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_req():
    """Filter each request before it is handled by the proper route"""
    excluded_endPoints = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]
    # if auth is None, do nothing
    if auth is not None:
        auth.require_auth(request.path, excluded_endPoints)
        cookie = auth.session_cookie(request)
        if auth.require_auth(request.path, excluded_endPoints):
            # Get authencaton credentials
            if auth.authorization_header(request) is None and cookie is None:
                abort(401)
            if auth.current_user(request) is None:
                abort(403)
            request.current_user = auth.current_user(request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
