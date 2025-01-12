import streamlit as st
import sqlite3
from argon2 import PasswordHasher

ph = PasswordHasher()

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('mental_health_app.db')
    return conn

# Function to create tables if they do not exist
def create_tables():
    conn = get_db_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')

# Function to create a new user
def create_user(username, password):
    conn = get_db_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
        if cursor.fetchone():
            return False  # Username already exists

        hashed_password = ph.hash(password)  # Hash the password with Argon2
        cursor.execute('INSERT INTO Users (username, password) VALUES (?, ?)', (username, hashed_password))
        return True  # User created successfully

# Function to log in a user
def login_user(username, password):
    conn = get_db_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM Users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user and ph.verify(user[0], password):  # Verify the password with Argon2
            return True  # Login successful
        return False  # Login failed