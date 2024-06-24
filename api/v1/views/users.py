#!/usr/bin/python3
"""api for user"""
from api.v1.views import app_views
import models
from models.user import User
from flask import abort, jsonify, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all user objects
    or a specific user
    """
    users = models.storage.all(User).values()
    list_users = []
    for user in users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves an user """
    user = models.storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """ add new user """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'username' not in request.get_json():
        abort(400, description="Missing username")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    instance = User(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """ Delete an user by id """
    user = models.storage.get(User, user_id)
    if not user:
        abort(404)
    models.storage.delete(user)
    models.storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates a user
    """
    user = models.storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    models.storage.save()
    return make_response(jsonify(user.to_dict()), 200)
