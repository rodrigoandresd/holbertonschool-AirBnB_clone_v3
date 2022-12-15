#!/usr/bin/python3
"""Module for State API endpoints"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def display_reviews(place_id):
    places = storage.all("Place", place_id)
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
    else:
        delete_review.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    new_review = request.get_json()
    if new_review is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_review:
        abort(400, 'Missing user_id')
    if 'text' not in new_review:
        abort(400, 'Missing text')
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    new_review = Review(user_id=request.json['user_id'],
                        text=request.json['text'], place_id=place_id)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    new_dict = request.get_json()
    if type(new_dict) is dict:
        review_obj = storage.get("Review", review_id)
        if review_obj is None:
            abort(404)
        for k, v in new_dict.items():
            if k not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
                setattr(review_obj, k, v)
            review_obj.save()
            return jsonify(review_obj.to_dict()), 200
    else:
        response = jsonify({"error": "Not a JSON"}), 400
        return response
