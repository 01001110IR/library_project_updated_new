from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate  # Import Migrate here
from books.customersmodel import Customer
from books.model import Book, db
from books.loansmodel import Loan

app = Flask(__name__, static_url_path='/library_project_updated/static')
CORS(app, origins="http://127.0.0.1:5501")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db.init_app(app)
migrate = Migrate(app, db)  # Move Migrate creation here

with app.app_context():
    db.create_all()
    
    
    
    
@app.route('/', methods=['GET'])
def renderindex():
    return render_template('index.html')


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#?                         BOOKS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    new_book = Book(name=data['name'], author=data['author'], year_published=data['year_published'], loan_type=data['loan_type'],stock = data['stock'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'}), 201

# Read all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = [{'id': book.id, 'name': book.name, 'author': book.author, 'year_published': book.year_published, 'loan_type': book.loan_type,'stock':book.stock } for book in books]
    return jsonify(book_list)

# Read a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'message': 'Book not found'}), 404
    return jsonify({'id': book.id, 'name': book.name, 'author': book.author, 'year_published': book.year_published, 'loan_type': book.loan_type,'stock':book.stock})

# Update a book by ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'message': 'Book not found'}), 404
    
    data = request.json
    book.name = data.get('name', book.name)
    book.author = data.get('author', book.author)
    book.year_published = data.get('year_published', book.year_published)
    book.loan_type = data.get('loan_type', book.loan_type)
    book.stock = data.get('stock', book.stock)

    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

# Delete a book by ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'message': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

@app.route('/books/delete-multiple', methods=['DELETE'])
def delete_multiple_books():
    data = request.get_json()
    book_ids = data.get('bookIds', [])  
    

    for book_id in book_ids:
        book = Book.query.get(book_id)
        if book is None:
            return jsonify({'message': 'Book not found'}), 404

        db.session.delete(book)

    db.session.commit()
        
    return jsonify(message='Selected books deleted successfully'), 200


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#?                         LOANS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@app.route('/loans', methods=['GET'])
def get_loans():
    loans = Loan.query.all()
    loan_list = []
    for loan in loans:
        loan_dict = {
            'id': loan.id,
            'book_id': loan.book_id,
            'customer_id': loan.customer_id,
            'additional_fields': loan.additional_fields  # Update to directly access the field
        }
        loan_list.append(loan_dict)
    return jsonify(loan_list)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import IntegrityError

from sqlalchemy.exc import IntegrityError  # Import IntegrityError

@app.route('/loans', methods=['POST'])
def create_loan():
    data = request.json
    book_id = data['book_id']
    customer_id = data['customer_id']

    # Check if the book is in stock
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    if book.stock is not None:
        if book.stock > 0:
            # Check if the customer has already borrowed this book
            existing_loan = Loan.query.filter_by(book_id=book_id, customer_id=customer_id, ).first()
            if existing_loan:
                return jsonify({'message': 'Customer has already borrowed this book'}), 400

            new_loan = Loan(
                book_id=book_id,
                customer_id=customer_id,
            )
            db.session.add(new_loan)
            try:
                db.session.commit()
                # Update book availability
                book.stock -= 1  # Decrease the stock
                return jsonify({'message': 'Loan created successfully'}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': 'IntegrityError: Book is already on loan'}), 400
        else:
            return jsonify({'message': 'Book is not available for loan'}), 400
    else:
        return jsonify({'message': 'Stock information is not available for this book'}), 400


@app.route('/loans/<int:loan_id>', methods=['PUT'])
def update_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if loan is None:
        return jsonify({'message': 'Loan not found'}), 404
    
    data = request.json
    # Update the loan fields
    loan.book_id = data.get('book_id', loan.book_id)
    loan.customer_id = data.get('customer_id', loan.customer_id)
    loan.additional_fields = data.get('additional_fields', loan.additional_fields)  # Include additional_fields

    db.session.commit()
    return jsonify({'message': 'Loan updated successfully'})




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#?                         CUSTOMERS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    customer_list = [{'id': customer.id, 'name': customer.name, 'id_number': customer.id_number, 'phone_number': customer.phone_number} for customer in customers]
    return jsonify(customer_list)

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    name = data.get('name')
    id_number = data.get('id_number')
    phone_number = data.get('phone_number')

    # Check if a customer with the provided id_number already exists
    existing_customer = Customer.query.filter_by(id_number=id_number).first()
    if existing_customer:
        return jsonify({'message': 'A customer with this id_number already exists'}), 400

    new_customer = Customer(name=name, id_number=id_number, phone_number=phone_number)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully'}), 201


@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify({'message': 'Customer not found'}), 404

    data = request.json
    name = data.get('name', customer.name)
    id_number = data.get('id_number', customer.id_number)
    phone_number = data.get('phone_number', customer.phone_number)

    customer.name = name
    customer.id_number = id_number
    customer.phone_number = phone_number

    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'})

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return jsonify({'message': 'Customer not found'}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})


@app.route('/customers/<int:id>', methods=['GET'])
def get_customer_by_id(id):
    customer = Customer.query.get(id)
    if customer is None:
        return jsonify({'message': 'Customer not found'}), 404
    customer_info = {'id': customer.id, 'name': customer.name, 'id_number': customer.id_number, 'phone_number': customer.phone_number}
    return jsonify(customer_info)








if __name__ == '__main__':
    app.run(debug=True)
