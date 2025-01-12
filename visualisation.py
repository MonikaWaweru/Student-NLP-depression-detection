import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

DATABASE_PATH = 'mental_health_app.db'


# Function to read data from the check-ins database
def read_checkin_data():
    with sqlite3.connect(DATABASE_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM MentalHealthCheckIns ORDER BY created_at DESC", conn)
    return df


# Function to read journal entries data
def read_journal_data():
    with sqlite3.connect(DATABASE_PATH) as conn:
        df = pd.read_sql_query("SELECT created_at, depression_risk_score FROM JournalEntries ORDER BY created_at DESC",
                               conn)
        # Explicitly convert created_at to datetime
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')  # Use 'coerce' to handle any invalid dates
    return df


# Function to get average scores from check-ins
def get_average_scores(conn):
    df2 = pd.read_sql_query(
        "SELECT AVG(feeling) as avg_feeling, AVG(serenity) as avg_serenity, "
        "AVG(sleep) as avg_sleep, AVG(productivity) as avg_productivity, "
        "AVG(enjoyment) as avg_enjoyment FROM MentalHealthCheckIns", conn)
    return df2.values[0]


# Function to clear data from the database
def clear_data():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM MentalHealthCheckIns")  # Clear check-ins
        cursor.execute("DELETE FROM JournalEntries")  # Clear journal entries
        conn.commit()


# Function to show visualizations
def show_visualization():
    with sqlite3.connect(DATABASE_PATH) as conn:
        # Generate visualizations for check-ins
        df_checkins = read_checkin_data()
        fig1 = px.line(df_checkins, x="created_at", y=["feeling", "serenity", "sleep", "productivity", "enjoyment"],
                       line_shape="spline", title="Mental Health Scores Over Time")
        fig1.update_layout(xaxis_tickformat='%Y-%m-%d')

        # Generate the visualization for depression risk scores
        df_journal = read_journal_data()

        # Scale and plot depression risk scores
        df_journal['depression_risk_score'] = df_journal['depression_risk_score'] * 10  # Scale to 1-10 if needed

        # Create a simple line chart for depression risk scores
        fig2 = px.line(df_journal, x="created_at", y="depression_risk_score",
                       title="Depression Risk Score Over Time",
                       labels={"depression_risk_score": "Depression Risk Score (1-10)"})
        fig2.update_layout(xaxis_tickformat='%Y-%m-%d', yaxis_title='Depression Risk Score (1-10)',
                           yaxis=dict(range=[0, 10]))  # Set y-axis range from 0 to 10

        # Get and plot the average scores
        average_scores = get_average_scores(conn)
        df3 = pd.DataFrame({
            "category": ["Feeling", "Serenity", "Sleep", "Productivity", "Enjoyment"],
            "average": average_scores
        })

        fig3 = px.bar_polar(df3, r="average", theta="category", template="plotly_dark")
        fig3.update_traces(opacity=0.7)
        fig3.update_layout(title="Average Mental Health Scores by Category")

    # Display the visualizations
    st.plotly_chart(fig1)  # Mental health scores over time
    st.plotly_chart(fig2)  # Simple depression risk score over time
    st.plotly_chart(fig3)  # Average scores by category


# Main function to run the visualization page
def visualisation_page():
    st.title("Mental Health Visualization")

    # Button to clear data
    if st.button("Clear Data"):
        clear_data()
        st.success("All data has been cleared.")

    show_visualization()

# Uncomment the following line if you wish to run this directly for testing:
# if __name__ == "__main__":
#     visualisation_page()