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
        st.write("Creating new users.csv file...")
        users_df = pd.DataFrame(columns=['username', 'password', 'email'])
        users_df.to_csv('users.csv', index=False)
        st.write("users.csv created successfully!")
    
    # Load Fashion Dataset
    if os.path.exists('Fashion Dataset.csv'):
        wardrobe_df = pd.read_csv('Fashion Dataset.csv')
        st.write("Fashion Dataset loaded successfully!")
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
        
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            if st.button("Login"):
                try:
                    users_df = pd.read_csv('users.csv')
                    # Debug information
                    st.write("Debug Info:")
                    st.write("- Entered username/email:", login_username)
                    st.write("- Entered password:", login_password)
                    st.write("- Available users in database:", users_df.to_dict('records'))
                    
                    # Check if username/email exists
                    user_exists = users_df[(users_df['username'] == login_username) | 
                                        (users_df['email'] == login_username)]
                    if user_exists.empty:
                        st.error(f"Account with username/email '{login_username}' not found")
                        return
                    
                    # Now check password
                    user = users_df[((users_df['username'] == login_username) | 
                                   (users_df['email'] == login_username)) & 
                                  (users_df['password'] == login_password)]
                    
                    if not user.empty:
                        st.session_state.logged_in = True
                        st.session_state.current_user = user.iloc[0]['username']
                        st.experimental_rerun()
                    else:
                        stored_password = user_exists.iloc[0]['password']
                        st.error(f"Incorrect password")
                        st.write(f"Debug - Stored password in database: {stored_password}")
                        
                except Exception as e:
                    st.error(f"Error during login: {str(e)}")
                    st.write("Full error details:", e)
        
        with col1_2:
            if st.button("Forgot Password"):
                try:
                    users_df = pd.read_csv('users.csv')
                    if login_username:
                        user = users_df[users_df['username'] == login_username]
                        if not user.empty:
                            st.info(f"Your password is: {user.iloc[0]['password']}")
                        else:
                            st.error("Username not found")
                    else:
                        st.warning("Please enter your username above")
                except Exception as e:
                    st.error(f"Error retrieving password: {str(e)}")

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
                    st.write("Debug - Updated users:", users_df['username'].tolist())
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
    to rent and borrow clothes effortlessly. List your outfits for rent, find suitable attire 
    for any occasion, and make fashion more accessible, cost-effective, and eco-friendly.
    """)

def show_wardrobe():
    st.header("My Wardrobe")
    
    try:
        # Load Fashion Dataset
        wardrobe_df = pd.read_csv('Fashion Dataset.csv')
        
        # Add search functionality
        search_query = st.text_input("🔍 Search items (by name, category, etc.)")
        
        # Filter based on search
        if search_query:
            filtered_df = wardrobe_df[
                wardrobe_df['name'].str.contains(search_query, case=False, na=False) |
                wardrobe_df['brand'].str.contains(search_query, case=False, na=False) |
                wardrobe_df['colour'].str.contains(search_query, case=False, na=False)
            ]
        else:
            filtered_df = wardrobe_df

        # Create a grid layout
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        # Display items in grid
        for idx, row in filtered_df.iterrows():
            with cols[idx % 3]:
                # Create a card for each item
                st.write("---")
                try:
                    st.image(row['img'], use_column_width=True)
                except:
                    st.warning("Image not available")
                
                st.markdown(f"""
                    <div style='background-color: white; padding: 10px; border-radius: 5px;'>
                        <h3 style='color: #1f1f1f;'>{row['name']}</h3>
                        <p style='color: #2E7D32; font-size: 24px;'>₹{row['price']}</p>
                        <p><b>Brand:</b> {row['brand']}</p>
                        <p><b>Color:</b> {row['colour']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Add to cart and wishlist buttons
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("🛒 Add to Cart", key=f"cart_{row['p_id']}"):
                        st.success("Added to cart!")
                with c2:
                    if st.button("❤️ Wishlist", key=f"wish_{row['p_id']}"):
                        st.success("Added to wishlist!")
        
        if filtered_df.empty:
            st.info("No items found matching your search.")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.write("Please check if the image URLs are accessible.")

def show_rent_items():
    st.header("Available Items for Rent")
    wardrobe_df = pd.read_csv('wardrobe.csv')
    available_items = wardrobe_df[
        (wardrobe_df['status'] == 'available') & 
        (wardrobe_df['owner'] != st.session_state.current_user)
    ]
    if not available_items.empty:
        st.dataframe(available_items)
    else:
        st.info("No items available for rent at the moment.")

def show_charity():
    st.header("Charity and Donations")
    st.write("""
    Help make a difference by donating your gently used clothing to those in need.
    Your donations can help support sustainable fashion and help those less fortunate.
    """)
    
    with st.form("donation_form"):
        item_description = st.text_area("Item Description")
        condition = st.selectbox("Item Condition", ["Like New", "Good", "Fair"])
        pickup_address = st.text_area("Pickup Address")
        submit_button = st.form_submit_button("Submit Donation")
        
        if submit_button:
            st.success("Thank you for your donation! We will contact you for pickup arrangements.")

def show_profile():
    st.header("My Profile")
    users_df = pd.read_csv('users.csv')
    user_data = users_df[users_df['username'] == st.session_state.current_user].iloc[0]
    
    st.write(f"Username: {user_data['username']}")
    st.write(f"Email: {user_data['email']}")
    
    if st.button("Edit Profile"):
        st.info("Profile editing feature coming soon!")

if __name__ == "__main__":
    main() 
