from ..db import db
import os



# TokenBlockedList Table
class TokenBlockedList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token= db.Column(db.String(250), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "token": self.token,
            "created_at": self.created_at
        }