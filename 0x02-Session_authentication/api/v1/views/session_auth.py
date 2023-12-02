#!/usr/bin/env python3
"""A module that handles all routes for the Session Authentication"""

@app_views.route('/auth_session/login/', methods=['POST'],
                    strict_slashes=False)
def auth_session():
    ""