from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year_published = db.Column(db.Integer)
    loan_type = db.Column(db.String(50))
