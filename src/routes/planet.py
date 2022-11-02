import os
from ..main import request, jsonify, app, bcrypt
from ..db import db
from ..models import User, Planets, Favorite_Planets
from flask import Flask, url_for
from datetime import datetime
import json


# Endpoint get all planets
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets), 200



# Endpoint get planet by id
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    if planet_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    planet = Planets.query.get(planet_id)
    if planet == None:
        raise APIException("Error: The planet does not exist", status_code=400)
    return jsonify(planet.serialize()), 200



# Endpoint post planet
@app.route('/planet', methods=['POST'])
def create_new_planet():
    body = request.get_json()
    # Validations
    if body is None:
        raise APIException("Error: body is empty", status_code=400)
    if body['name'] is None or body['name'] == "":
        raise APIException("Error: name is invalid", status_code=400)

    new_planets = Planets(name=body['name'], diameter=body['diameter'], rotation_Period=body['rotation_Period'], orbital_Period=body['orbital_Period'],
                          gravity=body['gravity'], population=body['population'], climate=body['climate'], terrain=body['terrain'], surface_Water=body['surface_Water'])
    planets = Planets.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))

    for i in range(len(planets)):
        if (planets[i]['name'] == new_planets.serialize()['name']):
            raise APIException("Error: The planet already exists", status_code=400)

    print(new_planets)
    #print(new_user.serialize())
    db.session.add(new_planets)
    db.session.commit()

    return jsonify({"mensaje": "Planet created successfully."}), 201



# Endpoint delete planet by id
@app.route('/planet/<int:item_id>', methods=['DELETE'])
def delete_planet_by_id(item_id):
    if item_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    planet = Planets.query.get(item_id)
    if planet == None:
        raise APIException("Error: the planet does not exist", status_code=400)
    db.session.delete(planet)
    db.session.commit()
    return jsonify("Planet successfully removed."), 200



# Endpoint delete from FAVORITE list => planet
@app.route('/favorites/planet/<int:item_id>', methods=['DELETE'])
def delete_favorite_planet_by_id(item_id):
    if item_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    item = Planets.query.get(item_id)
    if item == None:
        raise APIException("Error: the planet does not exist", status_code=400)
    db.session.delete(item)
    db.session.commit()
    return jsonify("Planet successfully removed."), 200



#Endpoint Update planet
@app.route('/planet/<int:planet_id>', methods=['PUT'])
def put_planet_by_id(planet_id):
    if planet_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    planet = Planets.query.get(planet_id)  
    if planet == None:
        raise APIException("Error: the planet does not exist", status_code=400)
    body = request.get_json()
    #Validation
    if body is None:
        raise APIException("Error: body is empty", status_code=400)
    # Check for body if empty (request)
    if not body['name'] is None:
        planet.name = body['name']
    db.session.commit()
    return jsonify(planet.serialize()), 200



#Endpoint Search people
@app.route('/planet/search', methods=['POST'])
def search_planet():
    body = request.get_json()
    #Validation
    if body is None:
        raise APIException("Error: body is empty", status_code=400)
    if not body['name'] is None:
        # find search query
        found = Planet.query.filter(Planet.name == body['name']).all()
        found = list(map(lambda item: item.serialize(), found))
        print(found)
    if found == None:
        raise APIException("Error: planet does not exist", status_code=400)
    return jsonify(found), 200