from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import json
import pymysql.cursors
import pymysql.cursors
from openai import OpenAI
from test_gpt import openai_chat
import os

app = Flask(__name__)
CORS(app)

"""with open('db_config.json', 'r') as config_file:
    db_config = json.load(config_file)

with open('openai_api_key.txt', 'r') as file:
    api_key = file.read().strip()

openai_client = OpenAI(api_key=api_key)"""

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
            story = cursor.fetchall()

        if story:
            # Call OpenAI API with the user's question and the story's truth
            combined_input = f"Question: {question}\n Surface Story: {story['surface_story']}\n Truth: {story['truth']}"
            prompt = ("Now you will receive a story and a question in the end of this prompt, and\
            your job is to read the story and find out if the answer to the question is \
            Yes or No. You can only output one of the following 4 options: 'Yes' (when the question asked matches\
            with what happened the story), 'No' (when the question asked is relevant about the story, but\
            the claim or its presupposition is erroneous or wrong), 'Maybe' (when the question asked is relevant to\
            the story but the claim is ambiguous and hard to deduce from the story alone if it is right or wrong), \
            'Irrelevant' (when the answer of the question is not explicitly included in the story, not in the form \
            of a question, or asking something completely irrelevant), or Many (the question involves too many questions\
            ). You should only output exactly one of the words ('Yes', 'No', 'Maybe', 'Irrelevant', 'Many‘) in all circumstances. You\
            will never provide an explanation." + '\n' + "The story and the question are as follows: " + combined_input)
            response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=10,
                seed=1234
            ).choices[0].message.content # TODO: Update with actual parameters needed for OpenAI API

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

    #connection = pymysql.connect(**db_config)
    connection = pymysql.connect(host = os.environ.get('HOST'), port = int(os.environ.get('PORT')), database = os.environ.get('DATABASE'), user = os.environ.get('USER'), password = os.environ.get('PASSWORD'))
    success = None
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Fetch the story's truth for validation
            cursor.execute("SELECT truth FROM stories WHERE id = %s", (story_id,))
            story = cursor.fetchone()

        if story:
            # Logic to determine if the guess is correct (this could be a simple string comparison or something more sophisticated)
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


if __name__ == '__main__':
    app.run(debug=True)