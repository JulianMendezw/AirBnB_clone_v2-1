#!/usr/bin/python3
""" Create a new view for user objects """

from flask import Flask
from models import storage
from api.v1.views import app_views
from models.user import User
from flask import make_response
from flask import jsonify
from flask import request


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id=None):
    """ get a user by id """

    dicty = storage.get(User, user_id)

    if dicty is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    else:
        return make_response(jsonify(dicty.to_dict()))


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_users():
    """ retrieve the list of all user objects"""

    mylist = []
    dicty_all = storage.all(User)

    for key, value in dicty_all.items():
        mylist.append(value.to_dict())

    return make_response(jsonify(mylist))


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id=None):
    """ Deleted if a object exist with code 200 otherwise raise error 404 """

    dicty = storage.get(User, user_id)

    if dicty:
        storage.delete(dicty)
        storage.save()
        return make_response(jsonify({}), 200)

    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Creates a user"""
    req = request.get_json()

    if req:
        if 'email' not in req:
            return make_response(jsonify("Missing email"), 400)
        if 'password' not in req:
            return make_response(jsonify("Missing password"), 400)
        else:
            new_user = User(**req)
            new_user.save()
            return make_response(jsonify(new_user.to_dict()), 201)
    else:
        return make_response(jsonify("Not a JSON"), 400)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    """ Update a user """

    req = request.get_json()
    if req:
        user = storage.get(User, user_id)

        if user:
            list_ignore = ["id", "email", "created_at", "update_at"]
            for key, value in req.items():
                if key not in list_ignore:
                    setattr(user, key, value)
            user.save()
            return make_response(jsonify(user.to_dict()), 200)

        else:
            return make_response(jsonify({"error": "Not found"}), 404)

    else:
        return make_response(jsonify("Not a JSON"), 400)
