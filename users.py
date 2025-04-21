import streamlit as st
import yaml
import os
from pathlib import Path
import hashlib
from datetime import datetime, timedelta
import secrets
import time

# Add this at the beginning of your app or in the main layout
st.markdown("""
    <style>
    /* Global button styles */
    .stButton > button {
        color: white !important;
        background-color: #0066FF !important;
        border-radius: 4px !important;
        padding: 0.5rem 1rem !important;
    }
    
    /* Specific styles for logout button */
    .stButton > button:hover {
        color: white !important;
        background-color: #0052CC !important;
        border-color: #0052CC !important;
    }
    
    /* File uploader styles */
    [data-testid="stFileUploader"] div[data-testid="stMarkdownContainer"] {
        color: rgba(250, 250, 250, 0.8) !important;
    }
    
    /* File upload box styles */
    [data-testid="stFileUploader"] div[data-testid="stFileUploadDropzone"] {
        background-color: white !important;
        border: 1px dashed #ccc !important;
        border-radius: 4px !important;
    }
    
    /* Uploaded file container */
    [data-testid="stFileUploader"] div[data-testid="stFileUploadDropzone"] > div:not(:first-child) {
        background-color: #0066FF !important;
        margin-top: 25px !important;
        border-radius: 4px !important;
        padding: 20px !important;
    }
    
    /* File name and details */
    [data-testid="stFileUploader"] div[data-testid="stFileUploadDropzone"] > div:not(:first-child) p,
    [data-testid="stFileUploader"] div[data-testid="stFileUploadDropzone"] > div:not(:first-child) div {
        color: white !important;
    }
    
    /* Close button in file uploader */
    [data-testid="stFileUploader"] button {
        color: white !important;
        background-color: transparent !important;
        border: none !important;
    }
    
    /* Drag and drop text */
    [data-testid="stFileUploader"] div[data-testid="stFileUploadDropzone"] > div:first-child {
        color: rgb(49, 51, 63) !important;
    }
    
    /* File size text */
    [data-testid="stFileUploader"] small {
        color: rgba(250, 250, 250, 0.8) !important;
    }
    
    /* Checkbox label color */
    .stCheckbox > label {
        color: rgb(49, 51, 63) !important;
    }
    
    /* Browse files button */
    [data-testid="stFileUploader"] div[data-testid="stFileUploadDropzone"] button {
        color: white !important;
        background-color: #0066FF !important;
        border-radius: 4px !important;
        padding: 0.5rem 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

def load_users():
    """Load users from users.yaml file"""
    users_file = Path('.streamlit/users.yaml')
    if users_file.exists():
        with open(users_file, 'r') as file:
            return yaml.safe_load(file)["users"]
    return {}

def save_users(users):
    """Save users to users.yaml file"""
    users_file = Path('.streamlit/users.yaml')
    users_file.parent.mkdir(exist_ok=True)
    with open(users_file, 'w') as file:
        yaml.dump({"users": users}, file)

def hash_password(password):
    """Create a hashed version of the password"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(username, password):
    users = load_users()
    if username in users:
        return users[username]["password_hash"] == hash_password(password)
    return False

def is_email_taken(email):
    """Check if the email is already registered"""
    users = load_users()
    return any(user.get('email') == email for user in users.values())

def register_user(username, password, email):
    """Register a new user"""
    users = load_users()
    
    if username in users:
        return False, "Username already exists!"
    
    if is_email_taken(email):
        return False, "Email address is already registered!"
    
    users[username] = {
        'password_hash': hash_password(password),
        'email': email,
        'created_at': datetime.now().strftime("%Y-%m-%d")
    }
    save_users(users)
    return True, "Registration successful!"

def generate_reset_token(username):
    """Generate a password reset token and store it with expiration"""
    users = load_users()
    if username not in users:
        return None
    
    token = secrets.token_urlsafe(32)
    expiration = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    
    users[username]["reset_token"] = {
        "token": token,
        "expiration": expiration
    }
    save_users(users)
    return token

def verify_reset_token(username, token):
    """Verify if the reset token is valid and not expired"""
    users = load_users()
    if username not in users or "reset_token" not in users[username]:
        return False
    
    token_data = users[username]["reset_token"]
    expiration = datetime.strptime(token_data["expiration"], "%Y-%m-%d %H:%M:%S")
    
    if token_data["token"] == token and datetime.now() < expiration:
        return True
    return False

def reset_password(username, new_password):
    """Reset the user's password and remove the reset token"""
    users = load_users()
    if username not in users:
        return False, "User not found"
    
    users[username]["password_hash"] = hash_password(new_password)
    if "reset_token" in users[username]:
        del users[username]["reset_token"]
    
    save_users(users)
    return True, "Password reset successful"

def get_user_by_email(email):
    """Find a user by their email address"""
    users = load_users()
    for username, user_data in users.items():
        if user_data.get("email") == email:
            return username
    return None

def show_login_page():
    """Display the login page and handle authentication."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None

    # Initialize the page state
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    if st.session_state.page == 'forgot_password':
        show_forgot_password_page()
        return False

    if not st.session_state.authenticated:
        st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .forgot-password {
            text-align: center;
            margin-top: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            st.markdown('<div class="login-header">', unsafe_allow_html=True)
            st.title("Welcome to AutoEDA")
            st.subheader("Please log in to continue")
            st.markdown('</div>', unsafe_allow_html=True)

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login", use_container_width=True):
                if verify_password(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            
            st.markdown('<div class="forgot-password">', unsafe_allow_html=True)
            if st.button("Forgot Password?", use_container_width=True):
                st.session_state.page = 'forgot_password'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

    return st.session_state.authenticated

def show_registration_form():
    st.markdown("""
    <style>
    .register-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .register-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="register-container">', unsafe_allow_html=True)
        st.markdown('<div class="register-header"><h2>Register New Account</h2></div>', unsafe_allow_html=True)
        
        new_username = st.text_input("Choose Username", key="reg_username")
        email = st.text_input("Email", key="reg_email")
        new_password = st.text_input("Choose Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")

        # Create Account button with unique key
        if st.button("Create Account", key="create_account_btn", use_container_width=True):
            # Validate all fields are filled
            if not new_username or not new_password or not email:
                st.error("All fields are required")
                return

            # Validate password confirmation
            if new_password != confirm_password:
                st.error("Passwords do not match")
                return

            # Basic email format validation
            if '@' not in email or '.' not in email:
                st.error("Please enter a valid email address")
                return

            # Check if username exists
            users = load_users()
            if new_username in users:
                st.error("Username already exists. Please choose a different username.")
                return

            # Check if email is taken
            if is_email_taken(email):
                st.error("Email address is already registered. Please use a different email.")
                return

            # If all validations pass, register the user
            success, message = register_user(new_username, new_password, email)
            if success:
                st.success(message)
                # Show additional success message with a delay
                with st.spinner("Redirecting to login..."):
                    time.sleep(2)  # Add a small delay for better UX
                st.session_state.page = 'login'
                st.rerun()
            else:
                st.error(message)
        
        # Add back to login option with unique key
        st.markdown("<div style='text-align: center; margin-top: 1rem;'>", unsafe_allow_html=True)
        st.write("Already have an account?")
        if st.button("Back to Login", key="reg_back_to_login_btn", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_logout_button():
    """Display the logout button in the sidebar."""
    # Add custom CSS for the logout button
    st.markdown("""
        <style>
        [data-testid="baseButton-secondary"][key="logout_btn"] {
            background-color: red !important;
            color: red !important;
            width: 100% !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
            border-radius: 4px !important;
        }
        /* Targeting sidebar buttons specifically */
        .stSidebar button {
            color: white !important;
            background-color: #0066FF !important;
            width: 100% !important;
        }

         
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.username:
        st.sidebar.markdown(f"Welcome, **{st.session_state.username}**!")
    
    if st.sidebar.button("Logout", key="logout_btn"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()

def show_forgot_password_page():
    """Display the simplified forgot password page"""
    st.markdown("""
    <style>
    .forgot-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="forgot-container">', unsafe_allow_html=True)
        st.title("Reset Password")
        
        # Step 1: User Identification
        identifier_type = st.radio("Search by:", ["Email", "Username"])
        
        if identifier_type == "Email":
            email = st.text_input("Enter your Email")
            if email:
                username = get_user_by_email(email)
                if not username:
                    st.error("Email not found")
                    return
        else:
            username = st.text_input("Enter your Username")
            if username:
                users = load_users()
                if username not in users:
                    st.error("Username not found")
                    return
        
        # Step 2: New Password (only shown if valid email/username was entered)
        if (identifier_type == "Email" and email and username) or (identifier_type == "Username" and username):
            st.divider()
            st.subheader("Set New Password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            if st.button("Reset Password", use_container_width=True):
                if not new_password or not confirm_password:
                    st.error("Please fill in all password fields")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    success, message = reset_password(username, new_password)
                    if success:
                        st.success(message)
                        st.session_state.page = 'login'
                        st.info("Please log in with your new password")
                        if st.button("Back to Login"):
                            st.rerun()
                    else:
                        st.error(message)
        
        # Add back to login button
        st.markdown("<div style='margin-top: 1rem;'>", unsafe_allow_html=True)
        if st.button("Back to Login", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_file_upload_section():
    """Display the file upload section with proper styling"""
    # Add custom CSS for the file uploader
    st.markdown("""
        <style>
        /* File uploader styling */
        .stFileUploader > div {
            background-color: white !important;
        }
        
        /* Uploaded file container */
        .stFileUploader > div > div:not(:first-child) {
            background-color: #0066FF !important;
            margin-top: 20px !important;
            padding: 20px !important;
            border-radius: 4px !important;
        }
        
        /* File name and details text */
        .stFileUploader > div > div:not(:first-child) p,
        .stFileUploader > div > div:not(:first-child) div {
            color: white !important;
        }
        
        /* Global button styling */
        .stButton > button {
            color: white !important;
            background-color: #0066FF !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Welcome, admin!")
    st.subheader("Upload Your CSV File Here")
    
    uploaded_file = st.file_uploader(
        "",
        type=["csv", "xls"],
        key="file_uploader",
        help="Limit 200MB per file • CSV, XLS"
    )
    
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    use_example = st.checkbox("Use Example Titanic Dataset")
    
    return uploaded_file, use_example

# Main app code
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None

# Add global CSS at the start of your app
st.markdown("""
    <style>
    /* Global button styles */
    .stButton > button {
        color: white !important;
        background-color: #0066FF !important;
    }
    
    /* Sidebar specific styles */
    .stSidebar .stButton > button {
        color: white !important;
        background-color: #0066FF !important;
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True) 