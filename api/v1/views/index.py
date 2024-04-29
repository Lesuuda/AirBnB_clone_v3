#!/usr/bin/pytho3
"""returns the JSON status report"""


from api.v1.views import app_views
from flask import Flask, jsonify


app = Flask(__name__)


@app_views.route('/status', strict_slashes=False)
def status():
    """return the status"""
    return jsonify({"status": "OK"})
