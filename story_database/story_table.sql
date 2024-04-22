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

ALTER TABLE user_story_attempts
DROP FOREIGN KEY user_story_attempts_ibfk_3;


INSERT INTO user_story_attempts (user_id, story_id, question_attempts, success, session_type, session_id) VALUES
(1, 10, 5, 1, 'single', 1001),
(1, 11, 7, 0, 'single', 1002),
(2, 10, 3, 1, 'single', 1003);

ALTER TABLE users ADD COLUMN firebase_uid VARCHAR(255) UNIQUE;

SELECT CONSTRAINT_NAME 
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS 
WHERE TABLE_NAME = 'users' AND CONSTRAINT_TYPE = 'UNIQUE';

ALTER TABLE users DROP INDEX `email`;

TRUNCATE TABLE game_sessions;
TRUNCATE TABLE user_story_attempts;
DELETE FROM users;

ALTER TABLE user_story_attempts ADD attempt_id INT AUTO_INCREMENT PRIMARY KEY;

ALTER TABLE user_story_attempts DROP FOREIGN KEY user_story_attempts_ibfk_1;
ALTER TABLE user_story_attempts MODIFY COLUMN user_id VARCHAR(255);
ALTER TABLE user_story_attempts ADD CONSTRAINT fk_user_firebase_uid FOREIGN KEY (user_id) REFERENCES users(firebase_uid) ON DELETE CASCADE;
ALTER TABLE user_story_attempts DROP INDEX if_exists_unique_index_name;
SHOW INDEXES FROM user_story_attempts;


ALTER TABLE user_story_attempts DROP INDEX if_exists_unique_index_on_user_id;

SHOW KEYS FROM user_story_attempts WHERE Key_name = 'PRIMARY';
ALTER TABLE user_story_attempts DROP PRIMARY KEY;

SELECT CONSTRAINT_NAME, TABLE_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE REFERENCED_TABLE_NAME = 'user_story_attempts' AND REFERENCED_COLUMN_NAME = 'user_id';

