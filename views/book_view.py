from flask import Blueprint, request, jsonify
from models.init_db import db
from models.all_models import Book

book_blueprint = Blueprint('book', __name__)

@book_blueprint.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
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

    if request.method == 'POST':
        data = request.json
        book_name = data.get('name')
        if not book_name:
            return jsonify({'error': 'Book name is required'}), 400
        new_book = Book(
            name=data.get('name'),
            author=data.get('author'),
            published_Year=data.get('published_Year'),  # Ensure this field is provided
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

@book_blueprint.route('/book/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'GET':
        return jsonify({
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'published_Year': book.published_Year,
            'book_Type': book.book_Type,            
            'active': book.active
        }), 200

    if request.method == 'PUT':
        data = request.json
        book.name = data.get('name', book.name)
        book.author = data.get('author', book.author)
        book.published_Year=data.get('published_Year',book.published_Year)
        book.book_Type = data.get('book_Type', book.book_Type)                
        book.active = data.get('active', book.active)
        db.session.commit()
        return jsonify({
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'published_Year': book.published_Year,
            'book_Type': book.book_Type,            
            'active': book.active
        }), 200

    if request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        return jsonify({}), 204
