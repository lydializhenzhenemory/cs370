-- Active: 1708197661893@@127.0.0.1@3306
CREATE DATABASE IF NOT EXISTS DetectAIveDB;
USE DetectAIveDB;

CREATE TABLE stories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    story_name VARCHAR(255),
    surface_story TEXT,
    truth TEXT
);