-- Active: 1710687991956@@detectaive.cj0cq200ykmx.us-east-2.rds.amazonaws.com@3306@detectaive
CREATE DATABASE IF NOT EXISTS DetectAIveDB;
USE DetectAIveDB;

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


CREATE TABLE multiplayer_sessions ( --tracking multiplayer sessions with user id, story id, whoes turn it is, and whether the session ended
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    story_id INT,
    current_turn_user_id INT,
    state ENUM('active', 'finished') NOT NULL DEFAULT 'active',
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
    FOREIGN KEY (current_turn_user_id) REFERENCES users(id) ON DELETE SET NULL
);
