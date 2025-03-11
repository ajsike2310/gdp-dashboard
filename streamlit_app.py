import streamlit as st
import pandas as pd
from PIL import Image
import os

# Set page config
st.set_page_config(
    page_title="e-STYLE",
    page_icon="👔",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

# Session State initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Create users.csv if it doesn't exist
try:
    if not os.path.exists('users.csv'):
        users_df = pd.DataFrame(columns=['username', 'password', 'email'])
        users_df.to_csv('users.csv', index=False)
    
    # Load Fashion Dataset
    if os.path.exists('Fashion Dataset.csv'):
        wardrobe_df = pd.read_csv('Fashion Dataset.csv')
    else:
        st.error("Fashion Dataset.csv not found! Please make sure the file exists in the same directory.")
except Exception as e:
    st.error(f"Error loading files: {str(e)}")

def main():
    if not st.session_state.logged_in:
        show_login_signup()
    else:
        show_main_app()

def show_login_signup():
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Login")
        login_username = st.text_input("Username or Email", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            try:
                users_df = pd.read_csv('users.csv')
                user = users_df[((users_df['username'] == login_username) | 
                               (users_df['email'] == login_username)) & 
                              (users_df['password'] == login_password)]
                
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user.iloc[0]['username']
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password")
            except Exception as e:
                st.error(f"Error during login: {str(e)}")
    
    with col2:
        st.header("Sign Up")
        new_username = st.text_input("Username", key="signup_username")
        new_password = st.text_input("Password", type="password", key="signup_password")
        new_email = st.text_input("Email", key="signup_email")
        if st.button("Sign Up"):
            try:
                if not new_username or not new_password or not new_email:
                    st.error("Please fill in all fields")
                    return
                
                users_df = pd.read_csv('users.csv')
                if new_username in users_df['username'].values:
                    st.error("Username already exists")
                else:
                    new_user = pd.DataFrame({
                        'username': [new_username],
                        'password': [new_password],
                        'email': [new_email]
                    })
                    users_df = pd.concat([users_df, new_user], ignore_index=True)
                    users_df.to_csv('users.csv', index=False)
                    st.success("Account created successfully! You can now login.")
            except Exception as e:
                st.error(f"Error during signup: {str(e)}")

def show_main_app():
    st.title(f"Welcome to e-STYLE, {st.session_state.current_user}!")
    
    menu = ["Home", "My Wardrobe", "Rent Items", "Charity", "Profile"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        show_home()
    elif choice == "My Wardrobe":
        show_wardrobe()
    elif choice == "Rent Items":
        show_rent_items()
    elif choice == "Charity":
        show_charity()
    elif choice == "Profile":
        show_profile()
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.experimental_rerun()

def show_home():
    st.header("Welcome to e-STYLE")
    st.write("""
    e-STYLE is a smart wardrobe solution that promotes fashion sustainability by enabling users 
    to rent and borrow clothes effortlessly.
    """)

def show_wardrobe():
    st.header("My Wardrobe")
    try:
        wardrobe_df = pd.read_csv('Fashion Dataset.csv')
        search_query = st.text_input("🔍 Search items")
        
        if search_query:
            filtered_df = wardrobe_df[wardrobe_df.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]
        else:
            filtered_df = wardrobe_df
        
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        for idx, row in filtered_df.iterrows():
            with cols[idx % 3]:
                st.image(row['img'], use_column_width=True)
                st.write(f"**{row['name']}**")
                st.write(f"Brand: {row['brand']}")
                st.write(f"Color: {row['colour']}")
                st.write(f"Price: ₹{row['price']}")
                st.button("🛒 Add to Cart", key=f"cart_{row['p_id']}")
                st.button("❤️ Wishlist", key=f"wish_{row['p_id']}")
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

def show_rent_items():
    st.header("Available Items for Rent")
    wardrobe_df = pd.read_csv('wardrobe.csv')
    available_items = wardrobe_df[(wardrobe_df['status'] == 'available') & (wardrobe_df['owner'] != st.session_state.current_user)]
    if not available_items.empty:
        st.dataframe(available_items)
    else:
        st.info("No items available for rent at the moment.")

def show_charity():
    st.header("Charity and Donations")

def show_profile():
    st.header("My Profile")
    users_df = pd.read_csv('users.csv')
    user_data = users_df[users_df['username'] == st.session_state.current_user].iloc[0]
    st.write(f"Username: {user_data['username']}")
    st.write(f"Email: {user_data['email']}")

if __name__ == "__main__":
    main()
