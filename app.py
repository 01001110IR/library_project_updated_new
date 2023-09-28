from flask import Flask, request, jsonify
from flask_cors import CORS
from books.model import Book,db

app = Flask(__name__)
CORS(app, origins="http://127.0.0.1:5501")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # Use SQLite for simplicity
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    new_book = Book(name=data['name'], author=data['author'], year_published=data['year_published'], loan_type=data['loan_type'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'}), 201

# Read all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = [{'id': book.id, 'name': book.name, 'author': book.author, 'year_published': book.year_published, 'loan_type': book.loan_type} for book in books]
    return jsonify(book_list)

# Read a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'message': 'Book not found'}), 404
    return jsonify({'id': book.id, 'name': book.name, 'author': book.author, 'year_published': book.year_published, 'loan_type': book.loan_type})

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


if __name__ == '__main__':
    app.run(debug=True)
