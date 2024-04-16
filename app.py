from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import json
import pymysql.cursors
import pymysql.cursors
from openai import OpenAI
from test_gpt import openai_chat, win_or_lose
import os

app = Flask(__name__)
CORS(app)

"""with open('db_config.json', 'r') as config_file:
    db_config = json.load(config_file)

with open('openai_api_key.txt', 'r') as file:
    api_key = file.read().strip()"""

openai_client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

@app.route('/')
def home():
    return "Welcome to the Story Game! Access /single_player to start a new game."

@app.route('/single_player', methods=['GET'])
def fetch_story():
    # Handling the GET request for fetching a random story
    #connection = pymysql.connect(**db_config)
    connection = pymysql.connect(host = os.environ.get('HOST'), port = int(os.environ.get('PORT')), database = os.environ.get('DATABASE'), user = os.environ.get('USER'), password = os.environ.get('PASSWORD'))
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT surface_story, truth, id FROM stories")
            result = cursor.fetchall()
            random_story = random.choice(result) if result else None
            return jsonify({"surface_story": random_story['surface_story'], "story_id": random_story['id']})
    finally:
        connection.close()


@app.route('/single_player/question', methods=['POST'])
def handle_question():
    data = request.get_json()
    question = data.get('question')
    story_id = data.get('story_id')
    user_id = data.get('user_id')  # Assuming you're passing the user ID

    #connection = pymysql.connect(**db_config)
    connection = pymysql.connect(host = os.environ.get('HOST'), port = int(os.environ.get('PORT')), database = os.environ.get('DATABASE'), user = os.environ.get('USER'), password = os.environ.get('PASSWORD'))
    response = None
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Fetch the story's truth based on the story_id from the database
            cursor.execute("SELECT surface_story, truth FROM stories WHERE id = %s", (story_id,))
            story = cursor.fetchone()

        if story:
            # Call OpenAI API with the user's question and the story's truth
            combined_input = f"Question: {question}\nTruth: {story['truth']}"
            response = openai_chat(question, story['truth'])  # TODO: Update with actual parameters needed for OpenAI API

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
    surface_prompt = data.get('surfacePrompt')
    user_id = data.get('user_id')

    #connection = pymysql.connect(**db_config)
    connection = pymysql.connect(host = os.environ.get('HOST'), port = int(os.environ.get('PORT')), database = os.environ.get('DATABASE'), user = os.environ.get('USER'), password = os.environ.get('PASSWORD'))
    success = None
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Fetch the story's truth for validation
            cursor.execute("SELECT truth FROM stories WHERE id = %s", (story_id,))
            story = cursor.fetchone()
            print(story['truth'])

        if story:
            # Logic to determine if the guess is correct
            result = win_or_lose(guess, story['truth'], surface_prompt)

            if result == "Correct" or result == "Incorrect":
                return jsonify({"is_correct": result})
            else:
                return jsonify({"is_correct": "Unexpected response. Prompt failed"})

            """"
            # Update the user_story_attempts table with the result of the guess
            with connection.cursor() as cursor:
                cursor.execute(
                    INSERT INTO user_story_attempts (user_id, story_id, question_attempts, success) 
                    VALUES (%s, %s, 1, %s) 
                    ON DUPLICATE KEY UPDATE 
                        question_attempts = question_attempts + 1, success = VALUES(success)
                , (user_id, story_id, success))
                connection.commit()

            
            """
        else:
            return jsonify({"error": "Story not found"}), 404
    except pymysql.MySQLError as e:
        print(e)
    finally:
        connection.close()

    return jsonify({"is_correct": result})

@app.route('/api/store_user', methods=['POST'])
def store_user():
    user_data = request.json
    #connection = pymysql.connect(**db_config)
    connection = pymysql.connect(host = os.environ.get('HOST'), port = int(os.environ.get('PORT')), database = os.environ.get('DATABASE'), user = os.environ.get('USER'), password = os.environ.get('PASSWORD'))
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

# @app.route('/end_game_session', methods=['POST'])
# def end_game_session():
#     # Get the JSON data sent from the frontend
#     session_data = request.get_json()
#     required_fields = ['session_id', 'user_id', 'story_id', 'session_type', 
#                        'session_status', 'question_count', 'guess_attempts', 'last_activity']
#     if not all(field in session_data for field in required_fields):
#         return jsonify({'status': 'error', 'message': 'Missing data'}), 400
#     connection = pymysql.connect(**db_config)
#     connection = pymysql.connect(host = os.environ.get('HOST'), port = int(os.environ.get('PORT')), database = os.environ.get('DATABASE'), user = os.environ.get('USER'), password = os.environ.get('PASSWORD'))

#     try:
#         with connection.cursor() as cursor:
#             sql = """
#             INSERT INTO game_sessions (session_id, user_id, story_id, session_type, 
#                                        session_status, question_count, guess_attempts, 
#                                        last_activity)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#             ON DUPLICATE KEY UPDATE
#             session_status = VALUES(session_status),
#             question_count = VALUES(question_count),
#             guess_attempts = VALUES(guess_attempts),
#             last_activity = VALUES(last_activity)
#             """
#             # Execute the SQL query
#             cursor.execute(sql, (session_data['session_id'], session_data['user_id'], session_data['story_id'], 
#                                  session_data['session_type'], session_data['session_status'], 
#                                  session_data['question_count'], session_data['guess_attempts'], 
#                                  session_data['last_activity']))
            
#             connection.commit()
            
#             return jsonify({'status': 'success', 'message': 'Session data updated successfully'})
            
#     except Exception as e:
#         connection.rollback()
#         return jsonify({'status': 'error', 'message': str(e)}), 500
#     finally:
#         connection.close()


@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    #connection = pymysql.connect(**db_config)
    connection = pymysql.connect(host = os.environ.get('HOST'), port = int(os.environ.get('PORT')), database = os.environ.get('DATABASE'), user = os.environ.get('USER'), password = os.environ.get('PASSWORD'))

    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT u.username, COUNT(usa.success) AS wins, AVG(usa.question_attempts) AS avg_attempts
            FROM users u
            JOIN user_story_attempts usa ON u.id = usa.user_id
            WHERE usa.success = 1
            GROUP BY u.username
            ORDER BY wins DESC, avg_attempts ASC, u.username ASC
            """
            cursor.execute(sql)
            leaderboard = cursor.fetchall()
            return jsonify(leaderboard)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)