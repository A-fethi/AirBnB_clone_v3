#!/usr/bin/python3
"""Flask route returns json status response"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """Returns a JSON"""
    data = {"status": "OK"}
    return jsonify(data)


@app_views.route("/stats")
def stats():
    """Retrieves the number of each objects by type"""
    data = {"amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")}
    return jsonify(data)
