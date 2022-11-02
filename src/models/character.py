from ..db import db
import os



# Characters Table
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Float)
    mass = db.Column(db.Float)
    hair_color  = db.Column(db.String(250))
    skin_color  = db.Column(db.String(250))
    eye_color  = db.Column(db.String(250))
    birth_year = db.Column(db.Integer)
    gender = db.Column(db.String(250))
    homeworld = db.Column(db.String(250))
    character_favorite = db.relationship("Favorite_Character", backref="characters")

# Serialize result
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld
        }

# Pivote Table: Characters-Favorites
class Favorite_Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))

    def serialize(self):
        return {
            "id": self.id,
            "user_email": User.query.get(self.user_id).serialize()['email'],
            "character_name": Character.query.get(self.character_id).serialize()['name']          
        }
