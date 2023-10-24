from flask_sqlalchemy import SQLAlchemy

from books.model import db

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    additional_fields = db.Column(db.String(255))  # Define the additional_fields attribute

    related_book = db.relationship('Book', backref='Loans')

    customer = db.relationship('Customer', backref='Loans')

    def __init__(self, book_id, customer_id, additional_fields=None):
        self.book_id = book_id
        self.customer_id = customer_id
        self.additional_fields = additional_fields
