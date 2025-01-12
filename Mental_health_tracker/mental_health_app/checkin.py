import streamlit as st
import sqlite3
import plotly.graph_objects as go
from datetime import datetime


# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('mental_health_app.db')  # Update with your database file path
    return conn


# Function to create the table if it doesn't exist
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MentalHealthCheckIns (
            checkin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            feeling INTEGER,
            serenity INTEGER,
            sleep INTEGER,
            productivity INTEGER,
            enjoyment INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
    ''')
    conn.commit()
    conn.close()


def mental_health_checkin(user_id):
    create_table()  # Ensure the table exists
    st.write("## Mental Health Check-In")

    # Define the questions
    questions = [
        "How are you feeling today? (0 = Terrible, 10 = Great)",
        "How would you rate your level of serenity today? (0 = Poorly, 10 = Very well)",
        "How well did you sleep last night? (0 = Poorly, 10 = Very well)",
        "How productive were you today? (0 = Not at all, 10 = Extremely productive)",
        "How much did you enjoy your day today? (0 = Not at all, 10 = Very much)"
    ]

    # List to store answers
    answers = []

    # Iterate through the questions and get user input
    for question in questions:
        answer = st.slider(question, 0, 10)
        answers.append(answer)

    # Calculate the average of the answers
    average = sum(answers) / len(answers)
    st.write(f"Your average mental health score today is **{average:.1f}**")

    # Create and display a gauge chart
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=average,
        mode="gauge+number",
        title={'text': "Mental Health Score"},
        gauge={
            'axis': {'range': [0, 10]},
            'steps': [
                {'range': [0, 2], 'color': "red"},
                {'range': [2, 4], 'color': "orange"},
                {'range': [4, 6], 'color': "yellow"},
                {'range': [6, 8], 'color': "lightgreen"},
                {'range': [8, 10], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': average
            }
        }
    ))

    st.plotly_chart(fig, use_container_width=True, height=50)

    # Get the current date
    now = datetime.now()
    date_string = now.strftime('%Y-%m-%d')

    # Button to submit the check-in
    if st.button('Submit Check-In'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO MentalHealthCheckIns (user_id, feeling, serenity, sleep, productivity, enjoyment)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, answers[0], answers[1], answers[2], answers[3], answers[4]))
        conn.commit()
        conn.close()

        st.success("Your mental health check-in has been submitted!")