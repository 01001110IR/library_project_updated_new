from flask import Blueprint, request, jsonify
from models.init_db import db
from models.all_models import Book

book_blueprint = Blueprint('book', __name__)

@book_blueprint.route('/books', methods=['GET', 'POST'])
@book_blueprint.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def books(book_id=None):
    if request.method == 'GET':
        if book_id is None:
            books = Book.query.all()
            book_list = [{
                'id': book.id,
                'name': book.name,
                'author': book.author,
                'published_Year': book.published_Year,
                'book_Type': book.book_Type,            
                'active': book.active
            } for book in books]
            return jsonify(book_list), 200
        else:
            book = Book.query.get_or_404(book_id)
            return jsonify({
                'id': book.id,
                'name': book.name,
                'author': book.author,
                'published_Year': book.published_Year,
                'book_Type': book.book_Type,            
                'active': book.active
            }), 200

    elif request.method == 'POST':
        data = request.json
        new_book = Book(
            name=data.get('name'),
            author=data.get('author'),
            published_Year=data.get('published_Year'),
            book_Type=data.get('book_Type'),            
            active=data.get('active', 'available')     
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify({
            'id': new_book.id,
            'name': new_book.name,
            'author': new_book.author,
            'published_Year': new_book.published_Year,
            'book_Type': new_book.book_Type,            
            'active': new_book.active
        }), 201

    elif request.method == 'PUT' and book_id is not None:
        book = Book.query.get_or_404(book_id)
        data = request.json
        for key, value in data.items():
            setattr(book, key, value)
        db.session.commit()
        return jsonify({
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'published_Year': book.published_Year,
            'book_Type': book.book_Type,            
            'active': book.active
        }), 200

    elif request.method == 'DELETE' and book_id is not None:
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return jsonify({}), 204

    return jsonify({'error': 'Method not allowed'}), 405
