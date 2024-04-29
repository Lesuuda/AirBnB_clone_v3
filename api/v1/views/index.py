#!/usr/bin/python3
"""returns the JSON status report"""


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage

app = Flask(__name__)


@app_views.route('/status', strict_slashes=False)
def status():
    """return the status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """returns the stats of all the objects in the db"""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
