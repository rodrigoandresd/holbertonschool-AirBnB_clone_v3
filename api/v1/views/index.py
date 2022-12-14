#!/usr/bin/python3
"""Index file for Flask blueprints"""


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def r_json():
    """a route that return JSON status """
    return jsonify(status='OK')


@app_views.route('/stats')
def display_stats():
    return jsonify({"amenities": storage.count("Amenity"),
                "cities": storage.count("City"),
                "places": storage.count("Place"),
                "reviews": storage.count("Review"),
                "states": storage.count("State"),
                "users": storage.count("User")})
