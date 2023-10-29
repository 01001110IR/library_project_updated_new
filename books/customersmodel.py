from flask_sqlalchemy import SQLAlchemy

from books.model import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    id_number = db.Column(db.String(20), nullable=False, unique=True)
    phone_number = db.Column(db.String(15))

