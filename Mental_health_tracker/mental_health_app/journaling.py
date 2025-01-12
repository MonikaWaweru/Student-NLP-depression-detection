import streamlit as st
import sqlite3
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('mental_health_app.db')  # Update with your database file path
    return conn

# Function to create the table if it doesn't exist
def create_journal_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS JournalEntries (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            entry_text TEXT NOT NULL,
            depression_risk_score FLOAT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
    ''')
    conn.commit()
    conn.close()

# Load the pre-trained model and tokenizer
model = RobertaForSequenceClassification.from_pretrained(r'C:\Users\monik\PycharmProjects\Mental_health_tracker\mental_health_app\student_dep_roberta')
tokenizer = RobertaTokenizer.from_pretrained(r'C:\Users\monik\PycharmProjects\Mental_health_tracker\mental_health_app\student_dep_roberta')
model.eval()  # Set the model to evaluation mode

def analyze_entry(entry_text):
    # Tokenize and prepare the input for the model
    inputs = tokenizer(entry_text, return_tensors='pt', padding=True, truncation=True, max_length=512)

    # Run the model to get the prediction
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    # Assuming the score is the softmax of the output logits
    probabilities = torch.softmax(logits, dim=1)
    depression_risk_score = probabilities[0][1].item()  # Assuming class 1 is "depressed"

    rounded_score = round(depression_risk_score, 2)

    return rounded_score

def journaling_page(user_id):
    create_journal_table()  # Ensure the table exists

    # Add custom CSS for a darker theme
    st.markdown("""
        <style>
            .stApp {
                background-color: #1c1c1c;
                color: #e0e0e0;
            }
            h2 {
                color: #e0e0e0;
            }
            .prompt {
                background-color: #2e2e2e;
                border-left: 5px solid #2196F3;
                padding: 10px;
                margin: 10px 0;
                color: #ffffff;
            }
            textarea {
                background-color: #2e2e2e;
                color: #ffffff;
                border: 1px solid #4a4a4a;
            }
            .submit-button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .submit-button:hover {
                background-color: #45a049;
            }
        </style>
    """, unsafe_allow_html=True)

    # Define journaling prompts
    prompts = [
        ("Transition and Change",
         "What recent changes have you experienced in your life or studies? How have these changes affected your feelings about school and your personal life?"),
        ("Academic Challenges",
         "Reflect on an academic challenge you faced this week. What strategies did you use to cope with the stress? How did it make you feel overall?"),
        ("Relationships and Emotional Well-being",
         "Think about your relationships with friends and family. How do they support or challenge your emotional well-being? Write about a recent interaction that stood out."),
        ("Family Challenges",
         "Describe a situation with your family that has been difficult recently. How did it impact your mood and focus on school? What steps can you take to address any stress?"),
        ("Writing and Communication",
         "Reflect on a time when you needed to express your thoughts or feelings but found it challenging. What held you back, and how can you improve your communication in the future?"),
        ("Social Issues",
         "Identify a social issue that is important to you. How does it impact your life or the lives of your peers? What can you do to raise awareness or support those affected?"),
        ("Financial and Housing Struggles",
         "Think about your current financial situation as a student. What worries you the most about finances or housing? How can you manage these concerns more effectively?"),
        ("Post-Graduation Struggles",
         "As you think about life after graduation, what are your biggest fears or uncertainties? Write about your hopes for the future and how you plan to navigate this transition.")
    ]

    # Create a list to hold all entries
    all_entries = []

    # Display prompts and collect responses
    for idx, (title, question) in enumerate(prompts):
        st.markdown(f"### {title}")
        st.markdown(f"<div class='prompt'>{question}</div>", unsafe_allow_html=True)

        # Add a unique key for each text_area using the index
        entry_text = st.text_area(f"Your response for '{title}':", height=150, key=f"entry_text_{idx}")
        all_entries.append(entry_text)

    # Button to submit all entries
    if st.button('Submit All Entries', key='submit_button'):
        for idx, entry_text in enumerate(all_entries):
            if entry_text:  # Check if the entry is not empty
                depression_risk_score = analyze_entry(entry_text)

                # Store the entry in the database
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO JournalEntries (user_id, entry_text, depression_risk_score)
                    VALUES (?, ?, ?)
                ''', (user_id, entry_text, depression_risk_score))
                conn.commit()
                conn.close()

        st.success("All journal entries have been submitted and analyzed!")

# Uncomment the following line if you wish to run this directly for testing:
# if __name__ == "__main__":
#     journaling_page(user_id)