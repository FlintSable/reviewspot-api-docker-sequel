import sys
import os
sys.path.insert(0, '..')

import unittest
from sqlalchemy.orm import sessionmaker
from app.models.models import Business, Review
from app.db.db_config import connect_with_connector
from sqlalchemy import text
# from dotenv import load_dotenv


class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        # load_dotenv(dotenv_path)

        print("Environment Variables Loaded in Unittest:")
        print("GOOGLE_APPLICATION_CREDENTIALS:", os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
        print("INSTANCE_CONNECTION_NAME:", os.getenv('INSTANCE_CONNECTION_NAME'))
        print("DB_NAME:", os.getenv('DB_NAME'))
        print("DB_USER:", os.getenv('DB_USER'))
        print("DB_PASSWORD:", os.getenv('DB_PASS'))
    
        cls.engine = connect_with_connector()
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()
        # Clean database once before all tests
        cls.session.query(Review).delete()
        cls.session.query(Business).delete()
        cls.session.commit()
        

    @classmethod
    def tearDownClass(cls):
        cls.session.rollback()
        cls.session.close()
        cls.engine.dispose()

    # def setUp(self):
    #     # Create a new session for each test
    #     self.session = self.Session()
    #     # Clean up database
    #     self.session.query(Business).delete()
    #     self.session.query(Review).delete()
    #     self.session.commit()

    def test_database_connection(self):
        result = self.session.execute(text('SELECT 1'))
        self.assertIsNotNone(result.fetchone())
        print("Database connection successful!")

    def test_create_business(self):
        business_data = {
            'name': 'Test Business',
            'description': 'This is a test business',
            'address': '123 Test Street',
            'phone': '123-456-7890',
            'owner_id': 'test_owner',
            'city': 'Burbank',
            'state': 'CA',
            'zip': '11111'
        }

        business = Business(**business_data)
        self.session.add(business)
        self.session.commit()

        self.assertIsNotNone(business.id)
        print(f'Created business with ID: {business.id}')



if __name__ == '__main__':
    unittest.main()