from flask_sqlalchemy import SQLAlchemy
from books.model import db  # Assuming you have a 'db' instance defined in your app

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    due_date = db.Column(db.String(10), nullable=False)
    
    book = db.relationship('Book', backref='loans')  # Define a relationship with the Book model
    customer = db.relationship('Customer', backref='loans')  # Define a relationship with the Customer model
