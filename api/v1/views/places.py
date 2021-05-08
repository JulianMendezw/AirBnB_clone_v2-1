#!/usr/bin/python3
""" Create a new view for Places objects """

from flask import Flask
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from flask import make_response
from flask import jsonify
from flask import request


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def all_places(city_id):
    """ retrieve the list of all City objects"""

    dicty = storage.get(City, city_id)

    if dicty is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    mylist = []
    dicty_all = storage.all(Place)

    for key, value in dicty_all.items():
        if value.city_id == city_id:
            mylist.append(value.to_dict())

    return make_response(jsonify(mylist))


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id=None):
    """ get a user by id """

    dicty = storage.get(Place, place_id)

    if dicty is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    else:
        return make_response(jsonify(dicty.to_dict()))


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id=None):
    """ Deleted if a object exist with code 200 otherwise raise error 404 """

    dicty = storage.get(Place, place_id)

    if dicty:
        storage.delete(dicty)
        storage.save()
        return make_response(jsonify({}), 200)

    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id=None):
    """ Creates a Place """

    dicty = storage.get(City, city_id)
    if dicty is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    req = request.get_json()
    if req:
        if 'user_id' not in req:
            return make_response(jsonify("Missing user_id"), 400)

        if 'name' not in req:
            return make_response(jsonify("Missing name"), 400)

        user = storage.get(User, req['user_id'])
        if user is None:
            return make_response(jsonify({"error": "Not found"}), 404)

        new_place = Place(**req)
        new_place.city_id = city_id
        new_place.save()

        return make_response(jsonify(new_place.to_dict()), 201)

    else:
        return make_response(jsonify("Not a JSON"), 400)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id=None):
    """ Update a place """

    place = storage.get(Place, place_id)
    if place is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    req = request.get_json()
    if req:
        place = storage.get(Place, place_id)
        if place is None:
            return make_response(jsonify({"error": "Not found"}), 404)

        list_ignore = ["id", "user_id", "city_id", "created_at", "update_at"]

        for key, value in req.items():
            if key not in list_ignore:
                setattr(place, key, value)
        place.save()
        return make_response(jsonify(place.to_dict()), 200)

    else:
        return make_response(jsonify("Not a JSON"), 400)
