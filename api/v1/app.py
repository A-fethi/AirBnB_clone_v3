#!/usr/bin/python3
"""Principale applications module"""
from models import storage
from flask import Flask, jsonify
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Removes the current SQLALchemy Session"""
    storage.close()


@app.errorhandler(404)
def not_found(exception):
    data = {"error": "Not found"}
    return jsonify(data)

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
