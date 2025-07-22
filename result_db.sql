CREATE DATABASE result_db;
USE result_db;

CREATE TABLE students (
    roll_no VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    math INT,
    science INT,
    english INT
);