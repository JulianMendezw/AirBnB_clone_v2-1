#!/usr/bin/python3
""" Create a new view for STate objects """

from flask import Flask
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from flask import make_response
from flask import jsonify
from flask import request


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenities():
    """ retrieve the list of all Amenity objects"""

    mylist = []
    dicty_all = storage.all(Amenity)

    for key, value in dicty_all.items():
        mylist.append(value.to_dict())

    return make_response(jsonify(mylist))


@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id=None):
    """ get a Amenity by id """

    dicty = storage.get(Amenity, amenity_id)

    if dicty is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    else:
        return make_response(jsonify(dicty.to_dict()))


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_aminity(amenity_id=None):
    """ Deleted if a object exist with code 200 otherwise raise error 404 """

    dicty = storage.get(Amenity, amenity_id)

    if dicty is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    else:
        storage.delete(dicty)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ Creates a Amenity"""
    req = request.get_json()

    if req:
        if req['name']:
            new_amenity = Amenity(**req)
            new_amenity.save()
            return make_response(jsonify(new_amenity.to_dict()), 201)

        else:
            return make_response(jsonify("Missing name"), 400)

    else:
        return make_response(jsonify("Not a JSON"), 400)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id=None):
    """ Update a amenity """

    req = request.get_json()

    if req:
        amenity = storage.get(Amenity, amenity_id)

        if amenity:

            list_ignore = ['id', 'created_at', 'updated_at']

            for key, value in req.items():
                if key not in list_ignore:
                    setattr(amenity, key, value)

            storage.save()
            return make_response(jsonify(amenity.to_dict()), 200)

        else:
            return make_response(jsonify({"error": "Not found"}), 404)

    else:
        return make_response(jsonify("Not a JSON"), 400)
