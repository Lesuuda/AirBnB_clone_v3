#!/usr/bin/python3
"""handles Place object operations"""


from flask import abort, jsonify, request
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views, storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """gets places by city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """gets place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates a place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


    @app_views.route('/places_search', methods=['POST'], strict_slashes=False)
    def search_places():
        """searches for places based on JSON body"""
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        states = data.get('states', [])
        cities = data.get('cities', [])
        amenities = data.get('amenities', [])
        
        places = []
        
        if not states and not cities and not amenities:
            places = storage.all(Place).values()
        else:
            if states:
                for state_id in states:
                    state = storage.get(State, state_id)
                    if state:
                        places.extend(state.places)
            
            if cities:
                for city_id in cities:
                    city = storage.get(City, city_id)
                    if city:
                        places.extend(city.places)
            
            if amenities:
                places = [place for place in places if all(amenity_id in place.amenities for amenity_id in amenities)]
        
        return jsonify([place.to_dict() for place in places])
