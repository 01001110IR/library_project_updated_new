from .init_db import db
from datetime import timedelta
from sqlalchemy import CheckConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship

class Loan(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    returnDate = db.Column(db.Date, nullable=True)
    maxReturnDate = db.Column(db.Date, nullable=True)  # Change nullable to True

    # Data Integrity: Define a ForeignKeyConstraint to enforce the relationship
    __table_args__ = (
        ForeignKeyConstraint(['book_id'], ['books.id']),  # Corrected foreign key reference
        ForeignKeyConstraint(['customer_id'], ['customers.customer_id']),
    )

    def __init__(self, book_id, customer_id, loan_date, returnDate=None):
        self.book_id = book_id
        self.customer_id = customer_id
        self.loan_date = loan_date
        self.returnDate = returnDate
        self.maxReturnDate = None  # Initialize with None

        # Fetch the book and update the maxReturnDate
        book = Book.query.get(book_id)
        if book:
            book.active = 'unavailable'  # Update the book's active status
            self.set_max_return_date(book, loan_date)  # Calculate maxReturnDate
            db.session.add(book)  # Add the updated book to the session

    def set_max_return_date(self, book, loan_date):
        """Calculate and set the maximum return date based on book type."""
        if book.book_Type == 1:
            self.maxReturnDate = loan_date + timedelta(days=10)
        elif book.book_Type == 2:
            self.maxReturnDate = loan_date + timedelta(days=5)
        elif book.book_Type == 3:
            self.maxReturnDate = loan_date + timedelta(days=2)
        else:
            # Default logic if none of the types match
            self.maxReturnDate = loan_date + timedelta(days=10)

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
