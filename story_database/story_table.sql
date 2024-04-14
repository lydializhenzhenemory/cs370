-- Active: 1710687991956@@detectaive.cj0cq200ykmx.us-east-2.rds.amazonaws.com@3306@detectaive
CREATE DATABASE IF NOT EXISTS DetectAIveDB;

CREATE TABLE stories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    story_name VARCHAR(255),
    surface_story TEXT,
    truth TEXT,
    average_attempts FLOAT DEFAULT 0
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE user_story_attempts (
    user_id INT,
    story_id INT,
    question_attempts INT,
    PRIMARY KEY (user_id, story_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

ALTER TABLE user_story_attempts DROP COLUMN guess_accuracy;

ALTER TABLE stories ADD COLUMN difficulty ENUM('easy', 'medium', 'hard') NOT NULL DEFAULT 'easy';

ALTER TABLE user_story_attempts
ADD COLUMN success BOOLEAN NOT NULL DEFAULT FALSE,
ADD COLUMN guess_accuracy FLOAT DEFAULT NULL;
ALTER TABLE user_story_attempts
ADD COLUMN session_type ENUM('single', 'multi') NOT NULL DEFAULT 'single',
ADD COLUMN session_id INT NULL,
ADD FOREIGN KEY (session_id) REFERENCES multiplayer_sessions(session_id) ON DELETE SET NULL;



CREATE TABLE multiplayer_sessions ( --tracking multiplayer sessions with user id, story id, whoes turn it is, and whether the session ended
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    story_id INT,
    current_turn_user_id INT,
    state ENUM('active', 'finished') NOT NULL DEFAULT 'active',
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
    FOREIGN KEY (current_turn_user_id) REFERENCES users(id) ON DELETE SET NULL
);


CREATE TABLE game_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    story_id INT NOT NULL,
    session_type ENUM('single', 'multi') NOT NULL,
    session_status ENUM('ongoing', 'won', 'lost') NOT NULL DEFAULT 'ongoing',
    is_guest BOOLEAN DEFAULT FALSE,
    expiration_time TIMESTAMP NULL,
    current_turn_user_id INT NULL,
    question_count INT DEFAULT 0,
    guess_attempts INT DEFAULT 0,
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (current_turn_user_id) REFERENCES users(id) ON DELETE SET NULL
);

ALTER TABLE game_sessions
ADD COLUMN last_activity TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;



CREATE TABLE daily_challenge (
    challenge_date DATE PRIMARY KEY,
    story_id INT,
    FOREIGN KEY (story_id) REFERENCES stories(id)
);


CREATE TABLE challenge_attempts (
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    story_id INT,
    challenge_date DATE,
    time_taken_seconds INT,
    questions_attempted INT,
    success TINYINT(1),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (story_id) REFERENCES stories(id),
    FOREIGN KEY (challenge_date) REFERENCES daily_challenge(challenge_date)
);

ALTER TABLE stories AUTO_INCREMENT = 1;
DELETE FROM stories WHERE id>100;
