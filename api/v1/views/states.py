#!/usr/bin/python3
"""Objects that handle all default RestFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route("/states/", methods=["GET"])
def get_all_states():
    """Retrieves the list of all State objects"""
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=["GET"])
def get_state_by_id(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=["DELETE"])
def delete_state_by_id(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/', methods=["POST"])
def post_state():
    """Creates a State"""
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    if 'name' not in json_data:
        abort(400, description="Missing name")
    new_state = State()
    new_state.name = json_data['name']
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=["PUT"])
def put_state(state_id):
    """Updates a State object"""
    json_data = request.get_json()
    state = storage.get(State, state_id)
    if not json_data:
        abort(400, description="Not a JSON")
    if state:
        for k, v in json_data.items():
            ignored_keys = ["id", "created_at", "updated_at"]
            if k not in ignored_keys:
                setattr(state, k, v)
        storage.save()
        return jsonify(state.to_dict()), 200
    abort(404)
