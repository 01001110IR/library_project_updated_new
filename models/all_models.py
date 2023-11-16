from .init_db import db
from datetime import timedelta
from sqlalchemy import CheckConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from datetime import datetime, timedelta

class Loan(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    returnDate = db.Column(db.Date, nullable=True)
    maxReturnDate = db.Column(db.Date, nullable=True)

    def __init__(self, book_id, customer_id, loan_date, returnDate=None):
        self.book_id = book_id
        self.customer_id = customer_id
        self.loan_date = loan_date
        self.returnDate = returnDate
        self.maxReturnDate = self.calculate_max_return_date(book_id, loan_date)

    def calculate_max_return_date(self, book_id, loan_date):
        book = Book.query.get(book_id)
        if book:
            # Logic to determine maxReturnDate based on book type
            if book.book_Type == 1:
                return loan_date + timedelta(days=10)
            elif book.book_Type == 2:
                return loan_date + timedelta(days=5)
            elif book.book_Type == 3:
                return loan_date + timedelta(days=2)
            else:
                return loan_date + timedelta(days=10)  # Default duration
        return None  # In case book is not found




class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    published_Year = db.Column(db.String(255), nullable=False)
    active = db.Column(db.String(20), default='available')
    book_Type = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('LENGTH(name) > 0', name='check_title_nonempty'),
    )

    loans = relationship('Loan', backref='book', lazy=True, cascade='all, delete-orphan')

    def __init__(self, name, author, published_Year, book_Type, active='available'):
        self.name = name
        self.author = author
        self.published_Year = published_Year
        self.book_Type = book_Type
        self.active = active

class Customer(db.Model):
    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True)  # Add 'customer_id' column
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(255), nullable=False)

    loans = relationship('Loan', backref='customer', lazy=True, cascade='all, delete-orphan')

    def __init__(self, name, age, city):
        self.name = name
        self.age = age
        self.city = city
        db.session.add(self)
        db.session.flush()  # Ensure the customer is added to the database and gets an ID
