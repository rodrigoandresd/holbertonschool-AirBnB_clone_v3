#!/usr/bin/python3
"""Index file for Flask blueprints"""


from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def r_json():
    """a route that return JSON status """
    return jsonify(status='OK')
