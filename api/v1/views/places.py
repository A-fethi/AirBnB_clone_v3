#!/usr/bin/python3
"""Objects that handle all default RestFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    list_places = []
    for place in places:
        list_places.append(place.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=["GET"],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a Place"""
    cit = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    if 'user_id' not in json_data:
        abort(400, description="Missing user_id")
    user_id = json_data['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if 'name' not in json_data:
        abort(400, description="Missing name")
    json_data['city_id'] = city_id
    new_place = Place(**json_data)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=["PUT"],
                 strict_slashes=False)
def put_place(place_id):
    """Updates a Place object"""
    json_data = request.get_json()
    place = storage.get(Place, place_id)
    if not json_data:
        abort(400, description="Not a JSON")
    if place:
        for k, v in json_data.items():
            ignored_keys = ["id", "user_id", "city_id",
                            "created_at", "updated_at"]
            if k not in ignored_keys:
                setattr(city, k, v)
        storage.save()
        return jsonify(place.to_dict()), 200
    abort(404)
