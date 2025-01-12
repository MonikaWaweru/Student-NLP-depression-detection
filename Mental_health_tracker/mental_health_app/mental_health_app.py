import sqlite3

try:
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('mental_health_app.db')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create Journal Prompts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS JournalPrompts (
        prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
        theme TEXT NOT NULL,
        prompt TEXT NOT NULL
    )
    ''')

    # Create Journal Entries table with depression risk score
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS JournalEntries (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        entry_text TEXT NOT NULL,
        depression_risk_score FLOAT,  -- New column for the depression risk score
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    ''')

    # Create Mental Health Check-In table
    cursor.execute('''
    works with CREATE TABLE IF NOT EXISTS MentalHealthCheckIns (
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

    # Create Collective Analysis table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CollectiveAnalysis (
        analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        period_start DATE,
        period_end DATE,
        average_depression_risk_score FLOAT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    ''')

    # Insert Journal Prompts
    prompts = [
        ("Transition and Change", "What recent changes have you experienced in your life or studies? How have these changes affected your feelings about school and your personal life?"),
        ("Academic Challenges", "Reflect on an academic challenge you faced this week. What strategies did you use to cope with the stress? How did it make you feel overall?"),
        ("Relationships and Emotional Well-being", "Think about your relationships with friends and family. How do they support or challenge your emotional well-being? Write about a recent interaction that stood out."),
        ("Family Challenges", "Describe a situation with your family that has been difficult recently. How did it impact your mood and focus on school? What steps can you take to address any stress?"),
        ("Writing and Communication", "Reflect on a time when you needed to express your thoughts or feelings but found it challenging. What held you back, and how can you improve your communication in the future?"),
        ("Social Issues", "Identify a social issue that is important to you. How does it impact your life or the lives of your peers? What can you do to raise awareness or support those affected?"),
        ("Financial and Housing Struggles", "Think about your current financial situation as a student. What worries you the most about finances or housing? How can you manage these concerns more effectively?"),
        ("Post-Graduation Struggles", "As you think about life after graduation, what are your biggest fears or uncertainties? Write about your hopes for the future and how you plan to navigate this transition.")
    ]

    # Insert prompts into the JournalPrompts table
    cursor.executemany('''
    INSERT INTO JournalPrompts (theme, prompt) VALUES (?, ?)
    ''', prompts)

    # Commit the changes
    conn.commit()

    print("Database and tables created successfully, and prompts inserted!")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    # Close the database connection
    if conn:
        conn.close()