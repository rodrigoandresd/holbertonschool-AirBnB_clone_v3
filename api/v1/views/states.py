#!/usr/bin/python3
"""Module for State API endpoints"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def display_states():
    states = storage.all("State").values()
    states_list = []
    for obj in states:
        states_list.append(obj.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def display_state(state_id):
    try:
        state_obj = storage.get("State", state_id)
        return jsonify(state_obj.to_dict())
    except:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    delete_state = storage.get('State', state_id)
    if not delete_state:
        abort(404)
    else:
        delete_state.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    new_dict = request.get_json()
    if type(new_dict) is dict:
        if "name" in new_dict.keys():
            state = State(name=new_dict["name"])
            for k, v in new_dict.items():
                setattr(state, k, v)
            state.save()
            return jsonify(state.to_dict()), 201
        else:
            response = jsonify({"error": "Missing Name"}), 400
            return response
    else:
            response = jsonify({"error": "Not a JSON"}), 400
            return response


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    new_dict = request.get_json()
    if type(new_dict) is dict:
        state_obj = storage.get("State", state_id)
        if state_obj is None:
            abort(404)
        for k, v in new_dict.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(state_obj, k, v)
            state_obj.save()
            return jsonify(state_obj.to_dict()), 200
    else:
        response = jsonify({"error": "Not a JSON"}), 400
        return response
