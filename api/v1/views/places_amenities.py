#!/usr/bin/python3
"""Objects that handle all default RESTFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from models import storage
from os import getenv


@app_views.route('/places/<place_id>/amenities/', methods=["GET"])
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = []
    if getenv("HBNB_TYPE_STORAGE") == "db":
        for amenity in place.amenities:
            amenities.append(amenity.to_dict())
    else:
        amenity_ids = place.amenity_ids
        for amenity_id in amenity_ids:
            amenities.append(storage.get(Amenity, amenity_id))
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=["DELETE"])
def delete_place_amenity(place_id, amenity_id):
    """Deletes an Amenity object from a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=["POST"])
def post_place_amenity(place_id, amenity_id):
    """Links an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
