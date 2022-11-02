import os
from ..main import request, jsonify, app, bcrypt
from ..db import db
from ..models import User
from flask import Flask, url_for
from datetime import datetime
import json


# Endpoint get all people
@app.route('/people', methods=['GET'])
def get_people():
    peoples = People.query.all()
    #print(users)
    peoples = list(map(lambda people: people.serialize(), peoples))
    #print(users)
    return jsonify(peoples), 200

# Endpoint get people by id
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    if people_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    person = People.query.get(people_id)
    if person == None:
        raise APIException("Error: Username does not exist", status_code=400)
    return jsonify(person.serialize()), 200



# Endpoint post people
@app.route('/people', methods=['POST'])
def create_new_person():
    body = request.get_json()
    # Validations
    if body is None:
        raise APIException("Error: body is empty", status_code=400)
    if body['name'] is None or body['name'] == "":
        raise APIException("Error: name is invalid", status_code=400)

    new_character = People(name=body['name'], height=body['height'], mass=body['mass'], hair_color=body['hair_color'], skin_color=body['skin_color'],
                           eye_color=body['eye_color'], birth_year=body['birth_year'], gender=body['gender'], homeworld=body['homeworld'])
    characters = People.query.all()
    characters = list(map(lambda character: character.serialize(), characters))

    print(new_character)
    #print(new_user.serialize())
    db.session.add(new_character)
    db.session.commit()

    return jsonify({"mensaje": "Character created successfully"}), 201



# Endpoint delete people by id
@app.route('/people/<int:item_id>', methods=['DELETE'])
def delete_character_by_id(item_id):
    if item_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    character = People.query.get(item_id)
    if character == None:
        raise APIException("Error: character does not exist", status_code=400)
    db.session.delete(character)
    db.session.commit()
    return jsonify("Character successfully deleted"), 200



# Endpoint DELETE drom FAVORITE people
@app.route('/favorites/people/<int:item_id>', methods=['DELETE'])
def delete_favorite_character_by_id(item_id):
    if item_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    item = People.query.get(item_id)
    if item == None:
        raise APIException("Error: character does not exist", status_code=400)
    db.session.delete(item)
    db.session.commit()
    return jsonify("Successfully deleted character."), 200



#Endpoint Update people
@app.route('/people/<int:people_id>', methods=['PUT'])
def put_people_by_id(people_id):
    if people_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    person = People.query.get(people_id)  
    if person == None:
        raise APIException("Error: Username does not exist", status_code=400)
    body = request.get_json()
    #Validation
    if body is None:
        raise APIException("Error: body is empty", status_code=400)
    # Check for body if empty (request)
    if not body['name'] is None:
        person.name = body['name']
    db.session.commit()
    return jsonify(person.serialize()), 200



#Endpoint Search people
@app.route('/people/search', methods=['POST'])
def search_people():
    body = request.get_json()
    #Validation
    if body is None:
        raise APIException("Error: body is empty", status_code=400)
    if not body['name'] is None:
        # va a encontrar todas las coincidencias
        found = People.query.filter(People.name == body['name']).all()
        found = list(map(lambda item: item.serialize(), found))
        print(found)
    if found == None:
        raise APIException("Error: character does not exist", status_code=400)
    return jsonify(found), 200