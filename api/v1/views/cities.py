#!/usr/bin/python3
"""Module for City API endpoints"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def display_cities(state_id):
    state_cities = storage.get("State", state_id)
    cities_list = []
    if state_cities:
        for obj in state_cities.cities:
            cities_list.append(obj.to_dict())
        return jsonify(cities_list)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def display_city(city_id):
    city_obj = storage.get("City", city_id)
    if city_obj:
        return jsonify(city_obj.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    city_obj = storage.get("City", city_id)
    if city_obj:
        storage.delete(city_obj)
        storage.save()
        response = jsonify({}), 200
        return response
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    new_dict = request.get_json(silent=True)
    if state_id not in [state.id for state in storage.all("State").values()]:
        abort(404)
    if type(new_dict) is dict:
        if "name" in new_dict.keys():
            city = City(name=new_dict["name"], state_id=state_id)
            for k, v in new_dict.items():
                setattr(city, k, v)
            city.save()
            return jsonify(city.to_dict()), 201
        else:
            response = jsonify({"error": "Missing Name"}), 400
            return response
    else:
            response = jsonify({"error": "Not a JSON"}), 400
            return response


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):

    new_dict = request.get_json(silent=True)
    if type(new_dict) is dict:
        city_obj = storage.get("City", city_id)
        if city_obj is None:
            abort(404)
        for k, v in new_dict.items():
            if k not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city_obj, k, v)
        city_obj.save()
        return jsonify(city_obj.to_dict()), 200
    else:
        response = jsonify({"error": "Not a JSON"}), 400
        return response
