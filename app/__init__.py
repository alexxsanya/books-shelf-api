import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy #, or_
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  def books_pagination(request, collection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1)*BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF
    f_books = [book.format() for book in collection]

    return f_books[start:end]

  @app.route('/books')
  def get_all_books():
    books = Book.query.order_by(Book.id).all()
    f_books = books_pagination(request, books)
    if f_books is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'books': f_books,
            'count': len(f_books)
        })


  @app.route('/books/<int:book_id>', methods=['PATCH'])
  def update_book_rating(book_id):
    rating = request.get_json()['rating']
    try:
        book = Book.query.get(book_id)
        book.rating = rating
        book.update()
        return jsonify({        
        'success': True,
        'status': 200,
        'updated': book_id
        })
    except:
        abort(422)

  @app.route('/books/<int:book_id>', methods=['DELETE'])
  def delete_book(book_id):
    try:
        book = Book.query.get(book_id)
        book.delete()
        return jsonify({        
        'success': True,
        'status': 200,
        'deleted': book.id
        })
    except:
        abort(404)

  @app.route('/books', methods=['POST'])
  def add_book():
    try:
      data = request.get_json()
      rating = int(data.get('rating', None))
      author = data.get('author', None)
      title = data.get('title', None)

      book = Book(title=title,author=author, rating=rating)
      book.insert()
        
      return jsonify({
        'success': True,
        'status': 201,
        'created': book.id
      })
    except:
      abort(400)

  return app

if __name__ == '__main__':
    app = create_app()
    app.run()