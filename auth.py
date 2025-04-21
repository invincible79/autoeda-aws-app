import streamlit as st
import hmac
import yaml
from yaml.loader import SafeLoader

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # First run, show inputs for username + password.
    if "password_correct" not in st.session_state:
        st.markdown("""
            <style>
            .auth-container {
                max-width: 400px;
                margin: 100px auto;
                padding: 2rem;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .auth-title {
                color: #1a237e;
                font-size: 1.8rem;
                font-weight: 600;
                margin-bottom: 1.5rem;
                text-align: center;
            }
            
            .auth-subtitle {
                color: #424242;
                font-size: 1rem;
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .stTextInput > div > div {
                background: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 0.5rem;
                margin-bottom: 1rem;
            }
            
            .stButton > button {
                background: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.6rem 1rem;
                width: 100%;
                font-weight: 500;
                margin-top: 1rem;
            }
            
            .stButton > button:hover {
                background: #1976D2;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            </style>
            
            <div class="auth-container">
                <div class="auth-title">Welcome to AutoEDA</div>
                <div class="auth-subtitle">Please enter your credentials to continue</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.text_input(
            "Username", key="username", placeholder="Enter your username"
        )
        st.text_input(
            "Password", type="password", key="password", placeholder="Enter your password"
        )
        st.button("Login", on_click=password_entered)
        return False
    
    # Password correct.
    if st.session_state["password_correct"]:
        return True
    
    # Password incorrect.
    st.error("😕 Password incorrect")
    st.button("Try again", on_click=password_entered)
    return False 