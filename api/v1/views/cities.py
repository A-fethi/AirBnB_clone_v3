#!/usr/bin/python3
"""Objects that handle all default RestFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route("/states/<state_id>/cities/", methods=["GET"])
def get_cities_by_id(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    list_cities = []
    for city in cities:
        list_cities.append(city.to_dict())
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=["GET"])
def get_city_by_id(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=["DELETE"])
def delete_city_by_id(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities/', methods=["POST"])
def post_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    if 'name' not in json_data:
        abort(400, description="Missing name")
    json_data['state_id'] = state_id
    new_city = City(**json_data)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["PUT"])
def put_city(city_id):
    """Updates a City object"""
    json_data = request.get_json()
    city = storage.get(City, city_id)
    if not json_data:
        abort(400, description="Not a JSON")
    if city:
        for k, v in json_data.items():
            ignored_keys = ["id", "state_id", "created_at", "updated_at"]
            if k not in ignored_keys:
                setattr(city, k, v)
        storage.save()
        return jsonify(city.to_dict()), 200
    abort(404)
