#!/usr/bin/python3
"""Module for State API endpoints"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def display_reviews(place_id):
    places = storage.get("Place", place_id)
    if places is None:
        abort(404)
    reviews = places.reviews
    reviews_list = []
    for obj in reviews:
        reviews_list.append(obj.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def display_review_id(review_id):
    try:
        review_obj = storage.get("Review", review_id)
        return jsonify(review_obj.to_dict())
    except:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_reviews(review_id):
    delete_review = storage.get('Review', review_id)
    if not delete_review:
        abort(404)
    delete_review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    my_place = storage.get('Place', place_id)
    if not my_place:
        abort(404)

    new_review = request.get_json()
    if not new_review:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_review:
        abort(400, 'Missing user_id')

    my_user = storage.get('User', new_review['user_id'])
    if not my_user:
        abort(404)

    if 'text' not in new_review:
        abort(400, 'Missing text')

    n_review = Review(**new_review)
    setattr(n_review, 'place_id', place_id)
    n_review.save()
    return jsonify(n_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    new_dict = request.get_json()
    if type(new_dict) is dict:
        review_obj = storage.get("Review", review_id)
        if review_obj is None:
            abort(404)
        for k, v in new_dict.items():
            if k not in ["id", "user_id", "place_id", "created_at",
                         "updated_at"]:
                setattr(review_obj, k, v)
        review_obj.save()
        return jsonify(review_obj.to_dict()), 200
    else:
        response = jsonify({"error": "Not a JSON"}), 400
        return response
