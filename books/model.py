from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year_published = db.Column(db.String(4), nullable=False)
    loan_type = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, default=0)  # Add the 'stock' attribute with a default value


