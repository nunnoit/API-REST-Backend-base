import os
from ..main import request, jsonify, app, bcrypt
from ..db import db
from ..models import User, Vehicles, Favorite_Vehicles
from flask import Flask, url_for
from datetime import datetime
import json

# Endpoint get all vehicles
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicles.query.all()
    vehicles = list(map(lambda vehicle: vehicle.serialize(), vehicles))
    return jsonify(vehicles), 200



# Endpoint get vehicle by id
@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle_by_id(vehicle_id):
    if vehicle_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    vehicle = Vehicles.query.get(vehicle_id)
    if vehicle == None:
        raise APIException("Error: The vehicle does not exist", status_code=400)
    return jsonify(vehicle.serialize()), 200



# Endpoint post vehicle
@app.route('/vehicle', methods=['POST'])
def create_new_vehicle():
    body = request.get_json()
    # Validations
    if body is None:
        raise APIException("Error: body is empty", status_code=400)
    if body['name'] is None or body['name'] == "":
        raise APIException("Error: name is invalid", status_code=400)

    new_vehicles = Vehicles(name=body['name'], model=body['model'], vehicle_class=body['vehicle_class'], manufacturer=body['manufacturer'], cost_in_credits=body['cost_in_credits'], length=body['length'],
                            crew=body['crew'], passengers=body['passengers'], max_atmosphering_speed=body['max_atmosphering_speed'], cargo_capacity=body['cargo_capacity'], consumables=body['consumables'])
    vehicles = Vehicles.query.all()
    vehicles = list(map(lambda vehicle: vehicle.serialize(), vehicles))

    for i in range(len(vehicles)):
        if (vehicles[i]['name'] == new_vehicles.serialize()['name']):
            raise APIException("The vehicle already exists", status_code=400)

    print(new_vehicles)
    db.session.add(new_vehicles)
    db.session.commit()

    return jsonify({"mensaje": "Vehicle created successfully"}), 201



# Endpoint vehicle planet by id
@app.route('/vehicle/<int:item_id>', methods=['DELETE'])
def delete_vehicle_by_id(item_id):
    if item_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    vehicle = Vehicles.query.get(item_id)
    if vehicle == None:
        raise APIException("Error: The vehicle does not exist.", status_code=400)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify("Vehicle removed successfully."), 200



# Endpoint DELETE drom FAVORITE vehicle
@app.route('/favorites/vehicle/<int:item_id>', methods=['DELETE'])
def delete_favorite_vehicle_by_id(item_id):
    if item_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    item = Vehicles.query.get(item_id)
    if item == None:
        raise APIException("Error: The vehicle does not exist", status_code=400)
    db.session.delete(item)
    db.session.commit()
    return jsonify("Vehicle removed successfully."), 200



#Endpoint Update vehicle
@app.route('/vehicle/<int:vehicle_id>', methods=['PUT'])
def put_vehicle_by_id(vehicle_id):
    if vehicle_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    vehicle = Vehicles.query.get(vehicle_id)  # Search by id
    if vehicle == None:
        raise APIException("Error: The vehicle does not exist", status_code=400)
    body = request.get_json()
    #Validation
    if body is None:
        raise APIException("Error: body is empty", status_code=400)
    # Check for body if empty (request)
    if not body['name'] is None:
        vehicle.name = body['name']
    db.session.commit()
    return jsonify(vehicle.serialize()), 200



#Endpoint Search vehicle
@app.route('/vehicle/search', methods=['POST'])
def search_vehicle():
    body = request.get_json()
    #Validation
    if body is None:
        raise APIException("Error: body is empty", status_code=400)
    if not body['name'] is None:
        # search in the db for the query
        found = Vehicles.query.filter(Vehicles.name == body['name']).all()
        found = list(map(lambda item: item.serialize(), found))
        print(found)
    if found == None:
        raise APIException("Error: vehicle does not exist", status_code=400)
    return jsonify(found), 200