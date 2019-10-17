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

if __name__ == '__main__':
    unittest.main()