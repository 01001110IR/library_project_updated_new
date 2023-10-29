from flask import Flask, render_template, request, jsonify, url_for
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
# Define a route to handle POST requests for creating loans
@app.route('/confirm_loan', methods=['POST'])
def handle_confirm_loan_request():
    data = request.json  # Assuming the data sent in the request is in JSON format
    # Add logic to create the loan, update the book stock, and respond with a success message
    # Replace the following with your actual logic:
    response_data = {'message': 'Loan created successfully'}  # Replace with the actual response data
    return jsonify(response_data), 201

# Borrow a book
@app.route('/borrow_book', methods=['POST'])
def borrow_book():
    data = request.json
    book_id = data.get('book_id')
    
    # Check if the book exists
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    # Check if the book is in stock
    if book.stock > 0:
        # Create a new loan
        new_loan = Loan(book_id=book_id, customer_id=data['customer_id'], due_date=data['due_date'])
        db.session.add(new_loan)
        
        # Reduce book stock
        book.stock -= 1
        db.session.commit()
        
        return jsonify({'message': 'Book borrowed successfully'}), 201
    else:
        return jsonify({'message': 'Book is out of stock'}), 400

# Return a book
@app.route('/return_book', methods=['POST'])
def return_book():
    data = request.json
    book_id = data.get('book_id')
    
    # Check if the book exists
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    # Check if the book is not already in stock
    if book.stock < book.total_stock:
        # Update the book stock and return the book
        book.stock += 1
        db.session.commit()
        
        # Delete the corresponding loan (assuming there is a loan associated with this book)
        loan = Loan.query.filter_by(book_id=book_id, customer_id=data['customer_id']).first()
        if loan:
            db.session.delete(loan)
            db.session.commit()
            
            return jsonify({'message': 'Book returned successfully'}), 200
        else:
            return jsonify({'message': 'No active loan found for this book and customer'}), 404
    else:
        return jsonify({'message': 'Book is already in stock'}), 400


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
