from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import json
import pymysql.cursors
from openai import OpenAI
from test_gpt import openai_chat
from apscheduler.schedulers.background import BackgroundScheduler
import pymysql
import datetime

app = Flask(__name__)
CORS(app)

with open('db_config.json', 'r') as config_file:
    db_config = json.load(config_file)

with open('openai_api_key.txt', 'r') as file:
    api_key = file.read().strip()

openai_client = OpenAI(api_key=api_key)

@app.route('/')
def home():
    return "Welcome to the Story Game! Access /single_player to start a new game."

@app.route('/single_player', methods=['GET'])
def fetch_story():
    # Handling the GET request for fetching a random story
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT surface_story, truth FROM stories")
            result = cursor.fetchall()
            random_story = random.choice(result) if result else None
            return jsonify({"surface_story": random_story['surface_story']})
    finally:
        connection.close()


@app.route('/single_player/question', methods=['POST'])
def handle_question():
    data = request.json
    question = data.get('question')
    story_id = data.get('story_id')
    user_id = data.get('user_id') 

    connection = pymysql.connect(**db_config)
    response = None
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Fetch the story's truth based on the story_id from the database
            cursor.execute("SELECT truth FROM stories WHERE id = %s", (story_id,))
            story = cursor.fetchone()

        if story:
            # Call OpenAI API with the user's question and the story's truth
            combined_input = f"Question: {question}\nTruth: {story['truth']}"
            response = openai_chat(combined_input)  # TODO: Update with actual parameters needed for OpenAI API

            # Increment the question_attempts count for the user-story pair in the user_story_attempts table
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO user_story_attempts (user_id, story_id, question_attempts) VALUES (%s, %s, 1) ON DUPLICATE KEY UPDATE question_attempts = question_attempts + 1", (user_id, story_id))
                connection.commit()
        else:
            return jsonify({"error": "Story not found"}), 404
    except pymysql.MySQLError as e:
        print(e)
    finally:
        connection.close()

    return jsonify({"response": response})

@app.route('/single_player/guess', methods=['POST'])
def handle_guess():
    data = request.json
    guess = data.get('guess')
    story_id = data.get('story_id')
    user_id = data.get('user_id')

    connection = pymysql.connect(**db_config)
    success = None
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Fetch the story's truth for validation
            cursor.execute("SELECT truth FROM stories WHERE id = %s", (story_id,))
            story = cursor.fetchone()

        if story:
            # Logic to determine if the guess is correct
            # button onclick --> guess
                # three attempts --> if failed first two, go back to game session
            is_correct = guess.lower().strip() == story['truth'].lower().strip()
            success = int(is_correct)

            # Update the user_story_attempts table with the result of the guess
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO user_story_attempts (user_id, story_id, question_attempts, success) 
                    VALUES (%s, %s, 1, %s) 
                    ON DUPLICATE KEY UPDATE 
                        question_attempts = question_attempts + 1, success = VALUES(success)
                """, (user_id, story_id, success))
                connection.commit()
        else:
            return jsonify({"error": "Story not found"}), 404
    except pymysql.MySQLError as e:
        print(e)
    finally:
        connection.close()

    return jsonify({"is_correct": success})

@app.route('/api/question', methods=['POST'])
def receive_question():
    question = request.json.get('question')
    # print to show we received user's question
    print("Received question:", question)
    # update response later when models are fine tuned
    return jsonify({'message': 'Question received successfully: ' + question})


@app.route('/api/store_user', methods=['POST'])
def store_user():
    user_data = request.json
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # Check if the user already exists in the database
            cursor.execute("SELECT id FROM users WHERE email = %s", (user_data['email'],))
            existing_user = cursor.fetchone()
            if existing_user:
                # If user exists, update their info
                cursor.execute("""
                    UPDATE users 
                    SET username = %s 
                    WHERE email = %s
                """, (user_data['name'], user_data['email']))
            else:
                # If not, insert the new user data
                cursor.execute("""
                    INSERT INTO users (username, email) 
                    VALUES (%s, %s)
                """, (user_data['name'], user_data['email']))
            connection.commit()
    except pymysql.MySQLError as e:
        connection.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        connection.close()

    return jsonify({"status": "success", "message": "User data stored successfully."})


if __name__ == '__main__':
    app.run(debug=True)
