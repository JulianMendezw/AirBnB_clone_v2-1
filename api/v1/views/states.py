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
@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states(state_id=None):
    """ retrieve the list of all State objects or one state by id """

    if (state_id):
        dicty = storage.get(State, state_id)

        if dicty is None:
            return make_response(jsonify({"error": "Not found"}), 404)

        else:
            dicty = dicty.to_dict()
            return make_response(jsonify(dicty))

    else:
        mylist = []
        dicty_all = storage.all(State)

        for key, value in dicty_all.items():
            mylist.append(value.to_dict())

        return make_response(jsonify(mylist))


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id=None):
    """ Deleted if a object exist with code 200 otherwise raise error 404 """
    key = "State.{}".format(state_id)
    dicty_all = storage.all(State)

    if key in dicty_all.keys():
        dicty = storage.get(State, state_id)
        dicty = dicty.delete()
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
def update_state(state_id=None):
    """ Update a State """

    req = request.get_json()

    if req:
        state = storage.get(State, state_id)
        setattr(state, 'name', req['name'])
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
    else:
        return make_response(jsonify("Not a JSON"), 400)
