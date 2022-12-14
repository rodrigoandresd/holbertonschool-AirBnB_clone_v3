#!/usr/bin/python3
"""Module for Amenity API endpoints"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def display_amenities():
    amenities = storage.all("Amenity").values()
    amenities_list = []
    for obj in amenities:
        amenities_list.append(obj.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def display_amenity(amenity_id):
    try:
        amenity_obj = storage.get("Amenity", amenity_id)
        return jsonify(amenity_obj.to_dict())
    except:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    delete_amenity = storage.get('Amenity', amenity_id)
    if delete_amenity:
        delete_amenity.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, 'Not a JSON')
    if 'name' not in new_amenity:
        abort(400, 'Missing name')
    new_amenity = Amenity(**new_amenity)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    new_dict = request.get_json()
    if type(new_dict) is dict:
        amenity_obj = storage.get("Amenity", amenity_id)
        if amenity_obj is None:
            abort(404)
        for k, v in new_dict.items():
            if k not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(amenity_obj, k, v)
        amenity_obj.save()
        return jsonify(amenity_obj.to_dict()), 200
    else:
        response = jsonify({"error": "Not a JSON"}), 400
        return response
