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
        }), 200


  @app.route('/books/<int:book_id>', methods=['PATCH'])
  def update_book_rating(book_id):
    try:
        rating = request.get_json()['rating']
        book = Book.query.get(book_id)
        book.rating = rating
        book.update()
        return jsonify({        
        'success': True,
        'status': 200,
        'updated': book_id
        }), 200
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
        }), 200
    except:
        abort(404)

  @app.route('/books', methods=['POST'])
  def add_book():
    data = request.get_json()
    rating = data.get('rating', None)
    author = data.get('author', None)
    title = data.get('title', None)
    search = data.get('search', None)

    try:
      if search:
        results = Book.query.order_by(Book.id).filter(Book.title.ilike(f'%{search}%'))
        f_books = books_pagination(request, results)

        return jsonify({
            'success': True,
            'books': f_books,
            'searched': search,
            'total_books': len(f_books)
        }), 200

      else:
        book = Book(title=title,author=author, rating=int(rating))
        book.insert()
          
        return jsonify({
          'success': True,
          'status': 201,
          'book': book.format(),
          'created': book.id
        }), 201
    except:
      abort(400)

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource Not Found'
    }), 404

  @app.errorhandler(405)
  def bad_request(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method Not Allowed'
    }), 405

  @app.errorhandler(422)
  def unprocessed(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Request Not Processed'
    }), 422

  @app.errorhandler(500)
  def bad_request(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Server Error'
    }), 500

  return app

if __name__ == '__main__':
    app = create_app()
    app.run()