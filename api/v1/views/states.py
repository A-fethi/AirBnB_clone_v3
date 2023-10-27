#!/usr/bin/python3
"""Objects that handle all default RestFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET"])
def get_all_states():
    """Retrieves the list of all State objects"""
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/<int:state_id>', methods=["GET"])
def get_state_by_id(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)
