#!/usr/bin/python3
"""Index file for Flask blueprints"""


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def r_json():
    """a route that return JSON status """
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def display_stats():
    result = {}
    cls_dict = {"Amenity": "amenities", "City": "cities", "Place": "places",
                "Review": "reviews", "State": "states", "User": "users"}

    for k, v in cls_dict.items():
        result[v] = storage.count(k)
    return jsonify(result)
