import os
from ..main import request, jsonify, app, bcrypt
from ..db import db
from ..models import User, TokenBlockedList
from flask import Flask, url_for
from datetime import datetime
import json
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

#Endpoint VIP Area (protected by user Token)
@app.route('/vip', methods=['post']) 
@jwt_required() # <--- Restricted by token
def page_protected():
    #claims = get_jwt()
    print("User ID: ", get_jwt_identity())
    user = User.query.get(get_jwt_identity()) # User id in the DB

    #get_jwt() Returns a dictionary
    jti=get_jwt()["jti"] 

    tokenBlocked = TokenBlockedList.query.filter_by(token=jti).first()

    if isinstance(tokenBlocked, TokenBlockedList):
        return jsonify(msg="Access denied")

    response_body={
        "message":"Token is valid :)",
        "user_id": user.id,
        "user_email": user.email
    }

    return jsonify(response_body), 200