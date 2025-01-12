import streamlit as st
from visualisation import visualisation_page
from journaling import journaling_page
from checkin import mental_health_checkin
from guidance import guidance_page
import os


def display_home_page():

    # Initialize session state if not already done
    if 'page' not in st.session_state:
        st.session_state.page = "home"

    # Sidebar for navigation
    with st.sidebar:
        # Load and display an image in the sidebar
        img_path = os.path.join(os.path.dirname(__file__), "images", "log.jpeg")  # Update path to your image
        st.image(img_path, width=300)  # Adjust width as necessary

        st.title("Navigation")
        # Radio button for section selection including Home
        page = st.radio("Select a section:",
                        ["Home", "Mental Health Check-In", "Journaling", "Visualisation", "Guidance"])

        # Logout button with custom styling
        if st.button("Logout", key="logout_button"):
            st.session_state.logged_in = False
            st.experimental_rerun()  # Refresh the app to show the login page

    # Custom CSS for red button
    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: red;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: darkred;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display content based on selected section
    if page == "Home":
        # Display the main content for the home page with smaller text
        st.subheader("Mental Health Awareness")
        st.write("""
        Mental health is crucial for overall well-being, especially for university students. 
        It's important to recognize the signs of mental health issues, such as anxiety, depression, and stress.
        """)

        st.subheader("Tips for Maintaining Mental Health")
        tips = [
            "1. Stay Active: Regular physical activity can boost your mood and energy levels.",
            "2. Stay Connected: Maintain relationships with friends and family.",
            "3. Practice Mindfulness: Engage in mindfulness or meditation to reduce stress.",
            "4. Get Enough Sleep: Prioritize sleep to enhance your focus and mood.",
            "5. Seek Help: Don’t hesitate to reach out for professional help if needed."
        ]
        for tip in tips:
            st.write(tip)

        st.subheader("Resources")
        st.write("""
        Here are some resources you can utilize:
        - **University Counseling Services**: Most universities offer counseling services for students.
        - **Mental Health Apps**: Consider using apps like Headspace or Calm for guided meditation.
        - **Hotlines**: If you're in crisis, reach out to local hotlines for immediate support.
        """)

        st.write("Remember, taking care of your mental health is just as important as your physical health.")

    elif page == "Mental Health Check-In":
        mental_health_checkin(st.session_state.user_id)
        # Call the function from the respective file
    elif page == "Journaling":
        journaling_page(st.session_state.user_id)  # Call the function from the respective file
    elif page == "Visualisation":
        visualisation_page()  # Call the function from the respective file
    elif page == "Guidance":
        guidance_page()  # Call the function from the respective file

# Uncomment the following line if you wish to run this directly for testing:
# if __name__ == "__main__":
#     display_home_page()