from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):    
    username = db.Column(db.String(50), unique=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False) 
    exp = db.Column(db.Integer, default=0) 
    risk_level = db.Column(db.Integer, default=1) 
    last_login = db.Column(db.DateTime, default=datetime.utcnow)  
    is_admin = db.Column(db.Boolean, nullable =False , default = False)
    achievements = db.relationship('UserAchievement', back_populates='user', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "exp": self.exp,
            "risk_level": self.risk_level,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "is_admin": self.is_admin
        }


class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    users = db.relationship('UserAchievement', back_populates='achievement', lazy=True)

class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user = db.relationship('User', back_populates='achievements')
    achievement = db.relationship('Achievement', back_populates='users')





