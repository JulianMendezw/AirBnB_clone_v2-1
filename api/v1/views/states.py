#!/usr/bin/python3
""" Create a new view for STate objects """

from flask import Flask
from models import storage
from api.v1.views import app_views
from models.state import State
from flask import make_response
from flask import jsonify
from flask import request


@app_views.route("/states/<state_id>")
@app_views.route("/states/")
def all_states(state_id=None):
    """ retrieve the list of all State objects """
    mylist = []
    if (state_id):
        dicty = storage.get(State, state_id)
        if dicty is None:
            res = make_response(jsonify({"error": "Not found"}), 404)
            return res
        else:
            dicty = dicty.to_dict()
            return dicty
    else:
        dicty_all = storage.all(State)
        for key, value in dicty_all.items():
            dicty_values = value.to_dict()
            mylist.append(dicty_values)
        return str(mylist)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id=None):
    """ return empty dictionary with status code 200 """
    key = "State.{}".format(state_id)
    dicty_all = storage.all(State)
    if key in dicty_all.keys():
        dicty = storage.get(State, state_id)
        dicty = dicty.delete()
        res = make_response(jsonify({}))
        return res
    res = make_response(jsonify({"error": "Not found"}), 404)
    return res


@app_views.route('/states/', methods=['POST'])
def post_state():
    """ Creates a State"""
    req = request.get_json()
    if typeof(req) == dict:

        return "___"
    res = make_response(jsonify({}), 201)
    return res
