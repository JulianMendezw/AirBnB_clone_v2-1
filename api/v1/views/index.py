#!/usr/bin/python3
""" Status json """
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import make_response, jsonify


@app_views.route('/status')
def return_json():
    """ Return a json status """
    res = make_response(jsonify({"status": "OK"}))
    return res


@app_views.route('/stats')
def return_stats():
    """ To get the number of objects by type """
    obj_classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }

    count_objs = {}

    for key, value in obj_classes.items():
        count_objs[key] = storage.count(value)

    return(make_response(jsonify(count_objs)))
