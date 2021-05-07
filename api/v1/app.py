#!/usr/bin/python3
""" Entrypoint of AIRBNB api """
import os
from flask import Flask
from models import storage
from flask import Blueprint
from api.v1.views import app_views
from flask import jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext_func(error):
    """ Close the session """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Custon error 404 handler """
    return (jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
