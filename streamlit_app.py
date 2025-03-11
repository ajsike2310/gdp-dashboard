import streamlit as st
import pandas as pd
import os

# Set up the page title and layout
st.set_page_config(page_title="E-Style - Smart Wardrobe", layout="wide")

# Apply custom CSS for styling
theme_color = "#074125"
st.markdown(
    f"""
    <style>
    .main {{
        background-color: black;
    }}
    .stButton>button {{
        background-color: {theme_color};
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px;
        transition: background-color 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #0b5e2b;
    }}
    .stTextInput>div>div>input {{
        border-radius: 10px;
        background-color: #222;
        color: white;
    }}
    .stImage>img {{
        border-radius: 10px;
    }}
    .menu-container {{
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 20px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.page = "Login"

# Dummy user database
users_db = {"user@example.com": "password123"}

def login(email, password):
    if email in users_db and users_db[email] == password:
        st.session_state.logged_in = True
        st.session_state.page = "Home"
        return True
    return False

def register_user(email, password):
    if email in users_db:
        return False
    users_db[email] = password
    return True

# Page Logic
if st.session_state.page == "Login":
    st.title("🔑 Login to E-Style")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_btn"):
        if login(email, password):
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials!")

elif st.session_state.page == "Sign Up":
    st.title("🆕 Create an E-Style Account")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
    if st.button("Sign Up", key="signup_btn"):
        if password == confirm_password:
            if register_user(email, password):
                st.success("Account created successfully!")
            else:
                st.error("Email already exists!")
        else:
            st.error("Passwords do not match!")

# Home Page (Only Visible After Login)
if st.session_state.logged_in:
    st.title("👗 Welcome to E-Style!")
    st.write("A smart wardrobe management system for organizing, renting, and styling outfits.")
    st.image("https://via.placeholder.com/800x400", caption="Smart Wardrobe Platform", use_column_width=True)

    # Navigation Menu on Home Screen
    st.markdown("<div class='menu-container'>", unsafe_allow_html=True)
    if st.button("My Wardrobe", key="wardrobe_btn"):
        st.session_state.page = "My Wardrobe"
    if st.button("AI Stylist", key="stylist_btn"):
        st.session_state.page = "AI Stylist"
    if st.button("Rentals", key="rentals_btn"):
        st.session_state.page = "Rentals"
    if st.button("Charity", key="charity_btn"):
        st.session_state.page = "Charity"
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.page == "My Wardrobe":
        st.title("👚 Your Wardrobe")
        uploaded_file = st.file_uploader("Upload an outfit image", type=["png", "jpg", "jpeg"], key="wardrobe_upload")
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Outfit", use_column_width=True)
            st.success("Image uploaded successfully!")
    
    elif st.session_state.page == "AI Stylist":
        st.title("🤖 Get Outfit Recommendations")
        occasion = st.selectbox("Select an occasion", ["Casual", "Formal", "Party", "Workout"], key="occasion_select")
        if st.button("Generate Outfit", key="stylist_generate"):
            st.image("https://via.placeholder.com/400", caption=f"Recommended {occasion} Outfit", use_column_width=True)

    elif st.session_state.page == "Rentals":
        st.title("🛒 Rent & Borrow Outfits")
        search = st.text_input("Search for an outfit", key="rental_search")
        if st.button("Search", key="rental_search_btn"):
            st.write(f"Showing results for: {search}")
            st.image("https://via.placeholder.com/400", caption="Available Outfit", use_column_width=True)
    
    elif st.session_state.page == "Charity":
        st.title("🎁 Donate Outfits for Charity")
        uploaded_file = st.file_uploader("Upload outfit to donate", type=["png", "jpg", "jpeg"], key="charity_upload")
        if st.button("Donate Now", key="charity_donate"):
            st.success("Thank you for your donation!")
