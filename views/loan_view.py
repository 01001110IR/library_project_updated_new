from flask import Blueprint, request, jsonify
from models.init_db import db
from models.all_models import Book, Loan
from datetime import datetime, timedelta 

loan_blueprint = Blueprint('loan', __name__)

@loan_blueprint.route('/loans', methods=['GET', 'POST'])
@loan_blueprint.route('/loan/<int:loan_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_loans(loan_id=None):
    if request.method == 'GET':
        if loan_id is None:
            # Get all loans
            loans = Loan.query.all()
            loan_list = [{
                'id': loan.id,
                'book_id': loan.book_id,
                'customer_id': loan.customer_id,
                'loan_date': loan.loan_date.isoformat(),
                'returnDate': loan.returnDate.isoformat() if loan.returnDate else None,
                'maxReturnDate': loan.maxReturnDate.isoformat() if loan.maxReturnDate else None
            } for loan in loans]
            return jsonify(loan_list), 200
        else:
            # Get a specific loan
            loan = Loan.query.get_or_404(loan_id)
            return jsonify({
                'id': loan.id,
                'book_id': loan.book_id,
                'customer_id': loan.customer_id,
                'loan_date': loan.loan_date.isoformat(),
                'returnDate': loan.returnDate.isoformat() if loan.returnDate else None,
                'maxReturnDate': loan.maxReturnDate.isoformat() if loan.maxReturnDate else None
            }), 200

    elif request.method == 'POST':
        # Borrow a book (Create a new loan)
        data = request.json
        book_id = data.get('book_id')
        customer_id = data.get('customer_id')
        loan_date = datetime.strptime(data.get('loan_date'), '%Y-%m-%d')

        new_loan = Loan(book_id=book_id, customer_id=customer_id, loan_date=loan_date)
        db.session.add(new_loan)
        book = Book.query.get(new_loan.book_id)
        book.active = 'Unavailable' 

        db.session.commit()
       
        return jsonify({
            'id': new_loan.id,
            'book_id': new_loan.book_id,
            'customer_id': new_loan.customer_id,
            'loan_date': new_loan.loan_date.isoformat(),
            'returnDate': new_loan.returnDate.isoformat() if new_loan.returnDate else None,
            'maxReturnDate': new_loan.maxReturnDate.isoformat() if new_loan.maxReturnDate else None
        }), 201
        
        
        
    elif request.method == 'DELETE':
         loan = Loan.query.get(loan_id)
         if loan is None:
          return jsonify({'message': 'Loan not found'}), 404
    
         db.session.delete(loan)
         db.session.commit()
         return jsonify({'message': 'Loan deleted successfully'}), 200

    
@loan_blueprint.route('/loan/<int:loan_id>/return', methods=['PUT'])
def return_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    loan.returnDate = datetime.now()  # Set the return date to now

    book = Book.query.get(loan.book_id)
    book.active = 'available'  # Update the book's status to available

    db.session.commit()
    return jsonify({'message': 'Book returned successfully'}), 200

