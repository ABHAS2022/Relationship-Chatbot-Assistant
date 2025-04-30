CREATE DATABASE IF NOT EXISTS chatapp;
USE chatapp;

-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    user_id CHAR(36) NOT NULL PRIMARY KEY,
    name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    identification_key_md5 TEXT
);

-- MESSAGES TABLE
CREATE TABLE IF NOT EXISTS messages (
    message_id VARCHAR(100) NOT NULL PRIMARY KEY,
    user_id CHAR(36),
    message_text TEXT,
    message_type TEXT,
    created_at TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP(6),
    message_order INT(11) NOT NULL UNIQUE AUTO_INCREMENT,
    thread_id VARCHAR(100),

    INDEX (user_id),
    INDEX (thread_id),

    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);