import os
from ..main import request, jsonify, app, bcrypt
from ..db import db
from ..models import User, Character, Favorite_Character
from flask import Flask, url_for
from datetime import datetime
import json


# Endpoint get all Characters
@app.route('/characters', methods=['GET'])
def get_character():
    characters = Character.query.all()
    #print(users)
    haracters = list(map(lambda character: character.serialize(), characters))
    #print(users)
    return jsonify(characters), 200

# Endpoint get Character by id
@app.route('/character/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
    if character_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    character = Character.query.get(character_id)
    if character == None:
        raise APIException("Error: Username does not exist", status_code=400)
    return jsonify(character.serialize()), 200



# Endpoint create new Character
@app.route('/character', methods=['POST'])
def create_new_character():
    body = request.get_json()
    # Validations
    if body is None:
        raise APIException("Error: body is empty", status_code=400)
    if body['name'] is None or body['name'] == "":
        raise APIException("Error: name is invalid", status_code=400)

    new_character = Character(name=body['name'], height=body['height'], mass=body['mass'], hair_color=body['hair_color'], skin_color=body['skin_color'],
                           eye_color=body['eye_color'], birth_year=body['birth_year'], gender=body['gender'], homeworld=body['homeworld'])
    characters = Character.query.all()
    characters = list(map(lambda character: character.serialize(), characters))

    print(new_character)
    #print(new_user.serialize())
    db.session.add(new_character)
    db.session.commit()

    return jsonify({"mensaje": "Character created successfully"}), 201



# Endpoint delete Character by id
@app.route('/character/<int:item_id>', methods=['DELETE'])
def delete_character_by_id(item_id):
    if item_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    character = Character.query.get(item_id)
    if character == None:
        raise APIException("Error: character does not exist", status_code=400)
    db.session.delete(character)
    db.session.commit()
    return jsonify("Character successfully deleted"), 200



# Endpoint DELETE drom FAVORITE Character
@app.route('/favorites/character/<int:item_id>', methods=['DELETE'])
def delete_favorite_character_by_id(item_id):
    if item_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    item = Character.query.get(item_id)
    if item == None:
        raise APIException("Error: character does not exist", status_code=400)
    db.session.delete(item)
    db.session.commit()
    return jsonify("Successfully deleted character."), 200



#Endpoint Update Character
@app.route('/character/<int:character_id>', methods=['PUT'])
def put_character_by_id(character_id):
    if character_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    character = Character.query.get(character_id)  
    if character == None:
        raise APIException("Error: Username does not exist", status_code=400)
    body = request.get_json()
    #Validation
    if body is None:
        raise APIException("Error: body is empty", status_code=400)
    # Check for body if empty (request)
    if not body['name'] is None:
        character.name = body['name']
    db.session.commit()
    return jsonify(character.serialize()), 200



#Endpoint Search Character
@app.route('/character/search', methods=['POST'])
def search_character():
    body = request.get_json()
    #Validation
    if body is None:
        raise APIException("Error: body is empty", status_code=400)
    if not body['name'] is None:
        found = Character.query.filter(Character.name == body['name']).all()
        found = list(map(lambda item: item.serialize(), found))
        print(found)
    if found == None:
        raise APIException("Error: character does not exist", status_code=400)
    return jsonify(found), 200