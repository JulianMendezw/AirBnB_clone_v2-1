#!/usr/bin/python3
""" Create a new view for STate objects """

from flask import Flask
from models import storage
from api.v1.views import app_views
from models.state import State
from flask import make_response
from flask import jsonify
from flask import request


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id=None):
    """ get a state by id """

    dicty = storage.get(State, state_id)

    if dicty is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    else:
        return make_response(jsonify(dicty.to_dict()))


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """ retrieve the list of all State objects"""

    mylist = []
    dicty_all = storage.all(State)

    for key, value in dicty_all.items():
        mylist.append(value.to_dict())

    return make_response(jsonify(mylist))


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id=None):
    """ Deleted if a object exist with code 200 otherwise raise error 404 """

    dicty = storage.get(State, state_id)

    if dicty:
        storage.delete(dicty)
        storage.save()
        return make_response(jsonify({}), 200)

    return make_response(jsonify({"error": "Not found"}), 404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a State"""
    req = request.get_json()

    if req:
        if req['name']:
            new_state = State(**req)
            new_state.save()
            return make_response(jsonify(new_state.to_dict()), 201)

        else:
            return make_response(jsonify("Missing name"), 400)

    else:
        return make_response(jsonify("Not a JSON"), 400)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    Updates a State
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
