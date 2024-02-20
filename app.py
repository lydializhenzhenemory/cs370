from flask import Flask, jsonify
from flask_cors import CORS
import random
import json
import pymysql.cursors

app = Flask(__name__)
CORS(app)

with open('db_config.json', 'r') as config_file:
    db_config = json.load(config_file)

@app.route('/')
def home():
    return "Welcome to the Story Game! Access /new_game to start a new game."

@app.route('/new_game', methods=['GET'])
def new_game():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT surface_story FROM stories")
            result = cursor.fetchall()
            random_story = random.choice(result) if result else None
            return jsonify(random_story)
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)