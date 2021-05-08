#!/usr/bin/python3
""" Create a new view for STate objects """

from flask import Flask
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City
from flask import make_response
from flask import jsonify
from flask import request


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def all_cities(state_id=None):
    """ retrieve the list of all State objects"""

    dicty = storage.get(State, state_id)

    if dicty is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    mylist = []
    dicty_all = storage.all(City)
    for key, value in dicty_all.items():
        if value.state_id == state_id:
            print(value.state_id)
            mylist.append(value.to_dict())

    return make_response(jsonify(mylist))


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id=None):
    """ get a city by id """

    dicty = storage.get(City, city_id)

    if dicty is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    else:
        return make_response(jsonify(dicty.to_dict()))


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id=None):
    """ Deleted if a object exist with code 200 otherwise raise error 404 """

    dicty = storage.get(City, city_id)

    if dicty:
        storage.delete(dicty)
        storage.save()
        return make_response(jsonify({}), 200)

    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id=None):
    """ Creates a City"""

    dicty = storage.get(State, state_id)

    if dicty is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    req = request.get_json()

    if req:
        if 'name' in req:
            new_city = City(**req)
            new_city.state_id = state_id
            new_city.save()
            return make_response(jsonify(new_city.to_dict()), 201)

        else:
            return make_response(jsonify("Missing name"), 400)

    else:
        return make_response(jsonify("Not a JSON"), 400)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    """ Update a State """

    req = request.get_json()

    if req:
        city = storage.get(City, city_id)
        if city:
            list_ignore = ["id", "state_id", "created_at", "update_at"]
            for key, value in req.items():
                if key not in list_ignore:
                    setattr(city, key, value)
            city.save()
            return make_response(jsonify(city.to_dict()), 200)

        else:
            return make_response(jsonify({"error": "Not found"}), 404)

    else:
        return make_response(jsonify("Not a JSON"), 400)
