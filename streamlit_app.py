import streamlit as st
import pandas as pd
import os

# Set up the page title and layout
st.set_page_config(page_title="E-Style - Smart Wardrobe", layout="wide")

# Apply custom CSS for improved styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    .stImage>img {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# Dummy user database
users_db = {"user@example.com": "password123"}

# Function to check login
def login(email, password):
    if email in users_db and users_db[email] == password:
        st.session_state.logged_in = True
        st.session_state.user_email = email
        return True
    return False

# Function to register user
def register_user(email, password):
    if email in users_db:
        return False
    users_db[email] = password
    return True

# Navigation menu
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Login", "Sign Up", "My Wardrobe", "AI Stylist", "Rentals", "Charity"])

# Home Page
if menu == "Home":
    st.title("👗 Welcome to E-Style!")
    st.write("A smart wardrobe management system for organizing, renting, and styling outfits.")
    st.image("https://via.placeholder.com/800x400", caption="Smart Wardrobe Platform", use_column_width=True)

# Login Page
elif menu == "Login":
    if st.session_state.logged_in:
        st.success(f"Logged in as {st.session_state.user_email}")
    else:
        st.title("🔑 Login to E-Style")
        email = st.text_input("Email", "")
        password = st.text_input("Password", "", type="password")
        if st.button("Login"):
            if login(email, password):
                st.success("Logged in successfully!")
            else:
                st.error("Invalid credentials!")

# Sign Up Page
elif menu == "Sign Up":
    st.title("🆕 Create an E-Style Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        if password == confirm_password:
            if register_user(email, password):
                st.success("Account created successfully!")
            else:
                st.error("Email already exists!")
        else:
            st.error("Passwords do not match!")

# My Wardrobe
elif menu == "My Wardrobe":
    if not st.session_state.logged_in:
        st.warning("Please login to access your wardrobe.")
    else:
        st.title("👚 Your Wardrobe")
        st.write("Upload and manage your outfits.")
        uploaded_file = st.file_uploader("Upload an outfit image", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Outfit", use_column_width=True)
            st.success("Image uploaded successfully!")

# AI Stylist
elif menu == "AI Stylist":
    if not st.session_state.logged_in:
        st.warning("Please login to use the AI Stylist.")
    else:
        st.title("🤖 Get Outfit Recommendations")
        occasion = st.selectbox("Select an occasion", ["Casual", "Formal", "Party", "Workout"])
        if st.button("Generate Outfit"):
            st.image("https://via.placeholder.com/400", caption=f"Recommended {occasion} Outfit", use_column_width=True)
            st.write("Here is a suggested outfit based on the occasion!")

# Rentals
elif menu == "Rentals":
    if not st.session_state.logged_in:
        st.warning("Please login to browse and rent outfits.")
    else:
        st.title("🛒 Rent & Borrow Outfits")
        st.write("Search and rent outfits from other users.")
        search = st.text_input("Search for an outfit")
        if st.button("Search"):
            st.write(f"Showing results for: {search}")
            st.image("https://via.placeholder.com/400", caption="Available Outfit", use_column_width=True)

# Charity Donations
elif menu == "Charity":
    if not st.session_state.logged_in:
        st.warning("Please login to donate outfits.")
    else:
        st.title("🎁 Donate Outfits for Charity")
        st.write("Help others by donating your unused outfits.")
        uploaded_file = st.file_uploader("Upload outfit to donate", type=["png", "jpg", "jpeg"])
        if st.button("Donate Now"):
            st.success("Thank you for your donation!")
