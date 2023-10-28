#!/usr/bin/python3
"""Objects that handle all default RestFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route("/users/", methods=["GET"])
def get_all_users():
    """Retrieves the list of all User objects"""
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=["GET"])
def get_user_by_id(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=["DELETE"])
def delete_user_by_id(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users/', methods=["POST"])
def post_user():
    """Creates a User"""
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    if 'email' not in json_data:
        abort(400, description="Missing email")
    if 'password' not in json_data:
        abort(400, description="Missing password")
    new_user = User(**json_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=["PUT"])
def put_user(user_id):
    """Updates a User object"""
    json_data = request.get_json()
    user = storage.get(User, user_id)
    if not json_data:
        abort(400, description="Not a JSON")
    if user:
        for k, v in json_data.items():
            ignored_keys = ["id", "email", "created_at", "updated_at"]
            if k not in ignored_keys:
                setattr(user, k, v)
        storage.save()
        return jsonify(user.to_dict()), 200
    abort(404)
