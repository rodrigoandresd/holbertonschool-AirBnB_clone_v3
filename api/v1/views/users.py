#!/usr/bin/python3
"""Module for users API endpoints"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def display_users():
    all_users = storage.all("User").values()
    users_list = []
    for obj in all_users:
        users_list.append(obj.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def display_user(user_id):
    try:
        user_obj = storage.get("User", user_id)
        return jsonify(user_obj.to_dict())
    except:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    delete_user = storage.get('User', user_id)
    if not delete_user:
        abort(404)
    else:
        delete_user.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    new_user = request.get_json()
    if new_user is None:
        abort(400, 'Not a JSON')
    if 'email' not in new_user:
        abort(400, 'Missing email')
    if 'password' not in new_user:
        abort(400, 'Missing password')
    new_user = User(email=request.json['email'],
                    password=request.json['password'])
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    new_dict = request.get_json(silent=True)
    if type(new_dict) is dict:
        user_obj = storage.get("User", user_id)
        if user_obj is None:
            abort(404)
        for k, v in new_dict.items():
            if k not in ["id", "email", "created_at", "updated_at"]:
                setattr(user_obj, k, v)
        user_obj.save()
        return jsonify(user_obj.to_dict()), 200
    else:
        response = jsonify({"error": "Not a JSON"}), 400
        return response
