import streamlit as st
import pandas as pd
import sqlite3

DATABASE_PATH = 'mental_health_app.db'


# Function to get the latest depression score from the database
def get_latest_depression_score():
    with sqlite3.connect(DATABASE_PATH) as conn:
        df = pd.read_sql_query("SELECT depression_risk_score FROM JournalEntries ORDER BY created_at DESC LIMIT 1",
                               conn)
    return df.iloc[0]['depression_risk_score'] if not df.empty else None


def guidance_page():
    st.title("Understanding Your Results")

    # Retrieve the latest depression score
    depression_score = get_latest_depression_score()

    if depression_score is not None:
        st.subheader("Your Latest Depression Risk Score")
        st.write(f"**Depression Risk Score:** {depression_score}")

        # Tailored guidance based on the score
        st.header("Guidance Based on Your Score")

        if depression_score < 5:
            st.write("Your score indicates that you are currently at a low risk of depression. "
                     "It's still important to maintain healthy habits and monitor your mental well-being.")
        elif 5 <= depression_score < 10:
            st.write("Your score suggests a moderate risk of depression. "
                     "Consider exploring self-help resources and possibly connecting with a mental health professional.")
        else:
            st.write("Your score indicates a high risk of depression. "
                     "We strongly encourage you to reach out to a mental health professional for support.")
    else:
        st.write("No depression score available. Please ensure you have recorded your journal entries.")

    st.header("Important Information About This Assessment")
    st.write(
        "This assessment is designed to help you understand your mental well-being. "
        "It is not a substitute for a professional diagnosis. The results you receive "
        "should be considered for informational purposes only, and you should consult "
        "with a mental health professional for personalized advice and treatment."
    )

    st.header("Next Steps")
    st.write(
        "- **Find a Therapist or Counselor**: Consider reaching out to a mental health professional who can provide personalized support.\n"
        "- **Explore Self-Help Resources**: Look into books, websites, and apps that can aid in improving your mental well-being.\n"
        "- **Connect with Support Groups**: Engaging with others who share similar experiences can provide valuable support."
    )

    st.header("Questions or Concerns?")
    st.write(
        "If you have any questions or concerns about your results or the assessment, please contact us via email at [support@example.com](mailto:support@example.com). We are here to help you find the right path to appropriate resources."
    )

    st.header("Privacy Policy")
    st.write(
        "We are committed to protecting your privacy. Read our full privacy policy [here]."
    )

# Uncomment the following line if you wish to run this directly for testing:
# if __name__ == "__main__":
#     guidance_page()