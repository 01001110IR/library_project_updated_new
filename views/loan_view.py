from flask import Blueprint, request, jsonify
from models.init_db import db
from models.all_models import Book, Loan
from datetime import datetime, timedelta 

loan_blueprint = Blueprint('loan', __name__)

@loan_blueprint.route('/loans', methods=['GET', 'POST'])
def loans():
    if request.method == 'GET':
        loans = Loan.query.all()
        loan_list = [{
            'id': loan.id,
            'book_id': loan.book_id,
            'customer_id': loan.customer_id,
            'loan_date': loan.loan_date.isoformat(),
            'returnDate': loan.returnDate.isoformat() if loan.returnDate else None,
            'maxReturnDate': loan.maxReturnDate.isoformat() if loan.maxReturnDate else None  # Add maxReturnDate
        } for loan in loans]
        return jsonify(loan_list), 200
    
    if request.method == 'POST':
        data = request.json
        book_id = data.get('book_id')
        book = Book.query.get(book_id)
        if not book or book.active != 'available':
            return jsonify({'error': 'Book is not available for loan'}), 400

        loan_date = datetime.strptime(data.get('loan_date'), '%Y-%m-%d')

        # Create a new loan
        new_loan = Loan(book_id=book_id, customer_id=data.get('customer_id'), loan_date=loan_date)

        db.session.add(new_loan)
        db.session.commit()

        return jsonify({
            'id': new_loan.id,
            'book_id': new_loan.book_id,
            'customer_id': new_loan.customer_id,
            'loan_date': new_loan.loan_date.isoformat(),
            'returnDate': new_loan.returnDate.isoformat() if new_loan.returnDate else None,
            'maxReturnDate': new_loan.maxReturnDate.isoformat()  # Add maxReturnDate
        }), 201

@loan_blueprint.route('/loan/<int:loan_id>', methods=['GET', 'PUT', 'DELETE'])
def loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)

    if request.method == 'GET':
        return jsonify({
            'id': loan.id,
            'book_id': loan.book_id,
            'customer_id': loan.customer_id,

            'returnDate': loan.returnDate  
        }), 200

    if request.method == 'PUT':
        data = request.json
        loan.book_id = data.get('book_id', loan.book_id)
        loan.customer_id = data.get('customer_id', loan.customer_id)

        loan.returnDate = data.get('returnDate', loan.returnDate)  
        db.session.commit()
        return jsonify({
            'id': loan.id,
            'book_id': loan.book_id,
            'customer_id': loan.customer_id,

            'returnDate': loan.returnDate  
        }), 200

    if request.method == 'DELETE':
        db.session.delete(loan)
        db.session.commit()
        return jsonify({}), 204

