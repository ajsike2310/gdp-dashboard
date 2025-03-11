import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(
    page_title="My Website",
    page_icon="🌐",
    layout="wide"
)

# Add a title
st.title("Welcome to My Website")

# Add a sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.selectbox("Go to:", ["Home", "About", "Contact"])

# Main content based on selection
if page == "Home":
    st.header("Home Page")
    st.write("Welcome to the home page of my website!")
    
    # Add some sample content
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Column 1")
        st.write("This is some content in column 1")
        st.button("Click Me!")
    
    with col2:
        st.subheader("Column 2")
        st.write("This is some content in column 2")
        st.metric(label="Sample Metric", value=42, delta=2)

elif page == "About":
    st.header("About Us")
    st.write("This is the about page. You can add your information here.")
    
    # Add an image
    st.image("https://placekitten.com/500/300", caption="Sample Image")

else:
    st.header("Contact Us")
    
    # Create a contact form
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submit = st.form_submit_button("Send Message")
        
        if submit:
            st.success("Thank you for your message! We'll get back to you soon.")

# Add a footer
st.markdown("---")
st.markdown("© 2024 My Website. All rights reserved.")
