from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    habits = db.relationship("Habit", backref="user", lazy=True)
    weight = db.Column(db.Float, nullable=True)  
    height = db.Column(db.Float, nullable=True)  
    age = db.Column(db.Integer, nullable=True)   
    gender = db.Column(db.String(10), nullable=True)  

class Habit(db.Model):
    __tablename__ = "Habits"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
    habit_name = db.Column(db.String(100), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    preferred_time = db.Column(db.String(20), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    completions = db.relationship("HabitCompletion", backref="habit", lazy=True)

class HabitCompletion(db.Model):
    __tablename__ = "HabitCompletions"

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("Habits.id"), nullable=False)
    date = db.Column(db.Date, default=datetime.now)
    completed = db.Column(db.Boolean, default=False)
