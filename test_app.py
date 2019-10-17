import os
import json
import unittest

from app import create_app
from models import setup_db, Book


class BookTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.db_name = 'bookshelf_test'
        self.db_path = 'postgresql://student:student@localhost:5432/{}'.format(self.db_name)
        setup_db(app=self.app,database_path=self.db_path)

        self.new_book = {
            'author': 'Alex Xsanya',
            'title': 'Beyond the Mix',
            'rating': 5
        }

    def tearDown(self):
        pass

    def test_paginated_books(self):
        res = self.client.get('/books')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True )
        self.assertLess(len(data), 8)

    def test_update_book_rating(self):
        book_id = 5
        res = self.client.patch(f'/books/{book_id}', json={'rating': 12})
        data = json.loads(res.data)
        book = Book.query.get(book_id)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 5)
        self.assertEqual(book.rating, 12)

    def test_422_unprocessed_book_update(self):
        book_id = 5000000
        res = self.client.patch(f'/books/{book_id}', json={'rating': 12})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request Not Processed')

    def test_delete_book(self):
        #first create a book to delete
        rs = self.client.post('/books', json = self.new_book)
        book = json.loads(rs.data)
        book_id = book['created'] #id of the book to be deleted

        res = self.client.delete(f'/books/{book_id}')
        data = json.loads(res.data)

        book = Book.query.filter(Book.id == book_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], book_id)
        self.assertEqual(book, None)

    def test_404_if_book_doesnt_exist(self):
        book_id = 69234
        res = self.client.delete(f'/books/{book_id}')
        data = json.loads(res.data)

        book = Book.query.filter(Book.id == book_id).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
        self.assertEqual(book, None)

    def test_add_book(self):
        res = self.client.post('/books', json = self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_405_if_method_not_allowed(self):
        res = self.client.post('/books/2334', json = self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')    

    def test_search_book(self):
        res = self.client.post('/books', json={'search' : 'Novel'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['searched'], 'Novel')
        self.assertTrue(data['books'])
        self.assertTrue(data['total_books'], 4)

    def test_search_book_no_results(self):
        res = self.client.post('/books', json={'search' : 'Balele'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['searched'], 'Balele')
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_books'], 0)

if __name__ == '__main__':
    unittest.main()