-- Active: 1708197661893@@localhost@3306@DetectAIveDB
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