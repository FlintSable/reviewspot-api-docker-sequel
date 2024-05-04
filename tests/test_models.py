import sys
sys.path.insert(0, '..')

import unittest
from sqlalchemy.orm import sessionmaker
from app.models.models import Business, Review
from app.db.db_config import connect_with_connector

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = connect_with_connector()
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        cls.engine.dispose()

    def test_database_connection(self):
        result = self.session.execute('SELECT 1')
        self.assertIsNotNone(result.fetchone())
        print("Database connection successful!")

    def test_create_business(self):
        business_data = {
            'name': 'Test Business',
            'description': 'This is a test business',
            'address': '123 Test Street',
            'phone': '123-456-7890',
            'owner_id': 'test_owner'
        }

        business = Business(**business_data)
        self.session.add(business)
        self.session.commit()

        self.assertIsNotNone(business.id)
        print(f'Created business with ID: {business.id}')

    # Add more test methods for other model operations

if __name__ == '__main__':
    unittest.main()