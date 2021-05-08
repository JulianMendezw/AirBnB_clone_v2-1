#!/usr/bin/python3
""" Create a new view for place objects """

from flask import Flask
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from flask import make_response
from flask import jsonify
from flask import request


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def all_reviews(place_id=None):
    """ retrieve the list of all place objects"""

    dicty = storage.get(Place, place_id)

    if dicty is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    mylist = []
    dicty_all = storage.all(Review)
    for key, value in dicty_all.items():
        if value.place_id == place_id:
            print(value.place_id)
            mylist.append(value.to_dict())

    return make_response(jsonify(mylist))


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id=None):
    """ get a review by id """

    dicty = storage.get(Review, review_id)

    if dicty is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    else:
        return make_response(jsonify(dicty.to_dict()))


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id=None):
    """ Deleted if a object exist with code 200 otherwise raise error 404 """

    dicty = storage.get(Review, review_id)

    if dicty:
        storage.delete(dicty)
        storage.save()
        return make_response(jsonify({}), 200)

    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id=None):
    """ Creates a review"""

    req = request.get_json()

    dicty_place = storage.get(Place, place_id)

    if dicty_place is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    if req:
        if 'user_id' not in req:
            return make_response(jsonify("Missing user_id"), 400)
        if 'text' not in req:
            return make_response(jsonify("Missing text"), 400)
        else:
            dicty_user = storage.get(User, req['user_id'])
            if dicty_user is None:
                return make_response(jsonify({"error": "Not found"}), 404)

            new_place = Place(**req)
            new_place.city_id = dicty_place.city_id
            new_place.name = dicty_place.name
            new_place.save()
            return make_response(jsonify(new_place.to_dict()), 201)

    else:
        return make_response(jsonify("Not a JSON"), 400)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id=None):
    """ Update a place """

    req = request.get_json()

    if req:
        review = storage.get(Review, review_id)
        print(review)
        if review:
            list_ignore = ["id", "user_id", "place_id", "created_at", "update_at"]
            for key, value in req.items():
                if key not in list_ignore:
                    setattr(review, key, value)
            review.save()
            return make_response(jsonify(review.to_dict()), 200)

        else:
            return make_response(jsonify({"error": "Not found"}), 404)

    else:
        return make_response(jsonify("Not a JSON"), 400)
