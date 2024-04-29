# Story Game API Documentation

Welcome to the Story Game API! Use these endpoints to interact with the story-based game.

## Endpoints

### Home (`/`)

- **Method**: GET
- **Description**: Home endpoint with welcome message.
- **Response**: A simple string welcoming users to the Story Game.

### Single Player Story Fetch (`/single_player`)

- **Method**: GET
- **Description**: Fetches a random story from the database for a single-player game.
- **Response**: JSON containing `surface_story` and `story_id`.

### Post Question (`/single_player/question`)

- **Method**: POST
- **Description**: Receives a question from a user and sends back a response.
- **Body**: JSON with `question`, `story_id`, and `user_id`.
- **Response**: JSON with `response` from ChatGPT.

### Guess Handling (`/single_player/guess`)

- **Method**: POST
- **Description**: Receives a guess from the user and checks for its correctness.
- **Body**: JSON with `guess`, `story_id`, `surfacePrompt`, and `user_id`.
- **Response**: JSON with the result of the guess, indicating `Correct` or `Incorrect`.

### Store User (`/api/store_user`)

- **Method**: POST
- **Description**: Stores or updates user information based on a unique Firebase ID.
- **Body**: JSON with user data including `name`, `email`, and `uid`.
- **Response**: JSON confirming the status of user data storage.

### Leaderboard (`/leaderboard`)

- **Method**: GET
- **Description**: Retrieves the leaderboard sorted by wins and average questions attempted.
- **Response**: JSON representing the leaderboard.

### Store Game Session (`/api/store_game_session`)

- **Method**: POST
- **Description**: Stores the data of a user's game session.
- **Body**: JSON with `id`, `win_or_lose`, `questions_attempted`, and `story_id`.
- **Response**: JSON confirming the status of game session data storage.

## Error Handling

All endpoints return appropriate status codes and messages in JSON format in case of errors. Common errors include:

- **404 Not Found**: When a requested story is not found.
- **400 Bad Request**: When user data is incorrect or incomplete.
- **500 Internal Server Error**: In case of database errors or unexpected conditions.

## Running the API

To run the API locally, execute the following command in your terminal:

```bash
python app.py
