import streamlit as st
from auth import create_tables, create_user, login_user
from home import display_home_page
from checkin import mental_health_checkin  # Import the check-in function
#from journaling import journaling_page  # Import the journaling function
#from visualization import visualization_page  # Import the visualization function
from guidance import guidance_page  # Import the guidance function

# Main app logic
def main():
    # Ensure tables are created when the app starts
    create_tables()

    # Initialize session state for page tracking
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_id = None  # Initialize user_id in session state
        st.session_state.current_page = "Home"  # Default page

    # Check if the user is logged in
    if st.session_state.logged_in:
        # Show the home page and handle navigation from it
        display_home_page()  # Home page should include navigation options
        show_page(st.session_state.current_page)  # Display the selected page
    else:
        login_page()  # Call your specific login function

def show_page(page):
    if page == "Mental Health Check-In":
        mental_health_checkin(st.session_state.user_id)  # Pass user_id to check-in
    elif page == "Journaling":
        journaling_page(st.session_state.user_id)  # Call journaling function
    elif page == "Visualization":
        visualization_page(st.session_state.user_id)  # Call visualization function
    elif page == "Guidance":
        guidance_page()  # Call guidance function

def login_page():
    st.title("Mental Health App - Authentication")

    # Option to sign up or log in
    option = st.selectbox("Select an option", ["Sign Up", "Login"])

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if option == "Sign Up":
        if st.button("Create Account"):
            if create_user(username, password):
                st.success("Account created successfully! You can now log in.")
            else:
                st.error("Username already exists. Please choose a different username.")

    elif option == "Login":
        if st.button("Log In"):
            user_id = login_user(username, password)
            if user_id:  # Assuming login_user returns the user_id on success
                # Set session state to indicate user is logged in
                st.session_state.logged_in = True
                st.session_state.user_id = user_id  # Store user_id in session state
                st.session_state.current_page = "Home"  # Set default page to Home
                st.success("Login successful! Redirecting to home page...")
                display_home_page()  # Refresh the app to show the home page
            else:
                st.error("Login failed. Please check your credentials.")

if __name__ == "__main__":
    main()