# test with python -m unittest discover tests
import unittest
from flask import json
import sys
import os
import pymysql

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from app import app

class FlaskAppTestCase(unittest.TestCase):


    def setUp(self):
        with open('db_config.json', 'r') as config_file:
            db_config = json.load(config_file)

        self.app = app.test_client()
        self.app.testing = True
        app.config['MYSQL_DATABASE_DB'] = 'detectaive'
        self.connection = pymysql.connect(**db_config)
        with self.connection.cursor() as cursor:
            # testing with user id 100 & story id 100, firstly insert into the tables
            cursor.execute("INSERT INTO users (id, username, password, email) VALUES (100, 'testuser', 'testpass', 'test@example.com') ON DUPLICATE KEY UPDATE id=id;")
            cursor.execute("INSERT INTO stories (id, story_name, surface_story, truth, average_attempts, difficulty) VALUES (100, 'Test Story', 'This is a surface story.', 'This is the truth.', 0, 'easy') ON DUPLICATE KEY UPDATE id=id;")
            cursor.execute("""
                INSERT INTO user_story_attempts (user_id, story_id, question_attempts, success) 
                VALUES (100, 100, 0, 0) ON DUPLICATE KEY UPDATE user_id=user_id;
            """)
            self.connection.commit()

    def tearDown(self):
        # Clean up the database
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM user_story_attempts WHERE user_id = 100 AND story_id = 100;")
            cursor.execute("DELETE FROM users WHERE id = 100;")
            cursor.execute("DELETE FROM stories WHERE id = 100;")
            self.connection.commit()
        self.connection.close()

    

    def test_handle_guess(self):
        test_data = {'guess': 'Your Guess', 'story_id': 100, 'user_id': 100}
        response = self.app.post('/single_player/guess', json=test_data)
        self.assertEqual(response.status_code, 200) #successful handling of the guess

if __name__ == '__main__':
    unittest.main()