#!/usr/bin/env python3
"""Basic flask app setup"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


Auth = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """The home page of the flask app"""
    return jsonify({"message", "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Endpoint for user registration"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        Auth.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Handles the login functionality"""
    email = request.form.get("email")
    password = request.form.get("password")
    valiid_user = Auth.valid_login(email, password)
    if not valiid_user:
        abort(401)
    session_id = Auth.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    # Cokkie set to client browser as session_id after successful login
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Handles the user logout functionality"""
    # Get Cookie from client browser as with the session id
    session_id = request.cookies.get("session_id")
    user = Auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    Auth.destroy_session(user_id)
    return redirect("/")


@app.route('/profile', methods=["GET"], strict_slashes=False)
def profile():
    """find user by session id"""
    session_id = request.cookies.get("session_id")
    user = Auth.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route('reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Get the token to reset password"""
    email = request.form.get('email')
    new_token = None
    try:
        new_token = Auth.get_reset_password_token(email)
    except ValueError:
        new_token = None
    if new_token is None:
        abort(403)
    return jsonify({"email": email, "reset_token": new_token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """Handles user's password update"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    is_password_updated = False
    try:
        Auth.update_password(reset_token, new_password)
        is_password_updated = True
    except ValueError:
        is_password_updated = False
    if not is_password_updated:
        abort(403)
    return jsonify({"email": email, "message": "password updated"})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
