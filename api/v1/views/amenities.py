#!/usr/bin/python3
"""Objects that handle all default RestFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities/", methods=["GET"])
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    all_amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in all_amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=["GET"])
def get_amenity_by_id(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"])
def delete_amenity_by_id(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities/', methods=["POST"])
def post_amenity():
    """Creates a Amenity"""
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    if 'name' not in json_data:
        abort(400, description="Missing name")
    new_amenity = Amenity()
    new_amenity.name = json_data['name']
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=["PUT"])
def put_amenity(amenity_id):
    """Updates a Amenity object"""
    json_data = request.get_json()
    amenity = storage.get(Amenity, amenity_id)
    if not json_data:
        abort(400, description="Not a JSON")
    if amenity:
        for k, v in json_data.items():
            ignored_keys = ["id", "created_at", "updated_at"]
            if k not in ignored_keys:
                setattr(amenity, k, v)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    abort(404)
