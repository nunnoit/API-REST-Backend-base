import os
from ..main import request, jsonify, app, bcrypt
from ..db import db
from ..models import User
from flask import Flask, url_for
from flask_jwt_extended import jwt_required
from datetime import datetime
import json

#Endpoint User register
@app.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()
    #print(body['username'])
    try:
        if body is None:
            raise APIException(
                "Invalid: Body is empty or email does not come in the body.", status_code=400)
        if body['email'] is None or body['email'] == "":
            raise APIException("Error: Email is valid.", status_code=400)
        if body['password'] is None or body['password'] == "":
            raise APIException("Error: password is invalid", status_code=400)

        password = bcrypt.generate_password_hash(
            body['password'], 10).decode("utf-8")

        new_user = User(email=body['email'], password=password, is_active=True)
        users = User.query.all()
        users = list(map(lambda user: user.serialize(), users))

        for i in range(len(users)):
            if (users[i]['email'] == new_user.serialize()['email']):
                raise APIException("Error: User already exists.", status_code=400)

        print(new_user)
        #print(new_user.serialize())
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"mensaje": "Usuario creado exitosamente"}), 201

    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"mensaje": "error al registrar usuario"}), 500



#Endpoint User login
@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body['email']
    password = body['password']

    user = User.query.filter_by(email=email).first()

    if user is None:
        raise APIException("Error: User does not exist", status_code=401)

    # Validate pass & check if match with user password in DB
    if not bcrypt.check_password_hash(user.password, password):
        raise APIException(
            "Error: Username or password do not match", status_code=401)

    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token})



# Endpoint user Logout
@app.route('/logout', methods=['get'])
@jwt_required()
def logout():
    print(get_jwt())
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)

    tokenBlocked = TokenBlockedList(token=jti, created_at=now)
    db.session.add(tokenBlocked)  # Add token to db to be blacklisted
    db.session.commit()

    return jsonify({"message": "The user has successfully logged out."})



# Endpoint suspend user
@app.route('/ban/<int:user_id>', methods=['PUT'])
@jwt_required()
def user_suspended(user_id):
    if get_jwt_identity() != 1:
        return jsonify({"message": "Operation not allowed"}), 403

    user = User.query.get(user_id)

    # Check if name come in the body request
    if user.is_active:
        user.is_active = False
        db.session.commit()
        return jsonify({"message": "User suspended"}), 203
    else:
        user.is_active = True
        db.session.commit()
        return jsonify({"message": "User is Active"}), 203



# Endpoint get all users
@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    #print(users)
    # (user)=>user.serialize()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200



# Endpoint Create new user
@app.route('/registration', methods=['POST'])
def create_new_user():
    body = request.get_json()
    #print(body['username'])
    descripcion = ""
    try:
        if body is None or "email" not in body:
            raise APIException(
                "Invalid: Body is empty or email does not come in the body.", status_code=400)
        if body['email'] is None or body['email'] == "":
            raise APIException("Error: Email is valid.", status_code=400)
        if body['password'] is None or body['password'] == "":
            raise APIException("Error: password is invalid", status_code=400)
        if body['description'] is None or body['description'] == "":
            descripcion = "Error: No description"
        else:
            descripcion = body['description']

        password = bcrypt.generate_password_hash(
            body['password'], 10).decode("utf-8")

        new_user = User(email=body['email'], password=password,
                        is_active=True, description=descripcion)
        users = User.query.all()
        users = list(map(lambda user: user.serialize(), users))

        for i in range(len(users)):
            if (users[i]['email'] == new_user.serialize()['email']):
                raise APIException(
                    "Error: User already exists.", status_code=400)

        print(new_user)
        #print(new_user.serialize())
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"mensaje": "User created successfully"}), 201

    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"mensaje": "Error registering user"}), 500



# Endpoint get user by id
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    if user_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    user = User.query.get(user_id)
    if user == None:
        raise APIException("Error: Username does not exist", status_code=400)
    #print(user.serialize())
    return jsonify(user.serialize()), 200



# Endpoint delete user by id
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    if user_id == 0:
        raise APIException("Error: id cannot be equal to 0", status_code=400)
    user = User.query.get(user_id)
    if user == None:
        raise APIException("Error: Username does not exist", status_code=400)
    #print(user.serialize())
    db.session.delete(user)
    db.session.commit()
    return jsonify("The user deleted successfully"), 200
