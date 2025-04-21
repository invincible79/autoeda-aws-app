import streamlit as st
from auth_cognito import cognito_auth

def show_login_page():
    st.markdown("""
        <style>
        .auth-form {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .form-header {
            text-align: center;
            margin-bottom: 2rem;
            color: #1a237e;
        }
        .form-subheader {
            text-align: center;
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }
        .password-requirements {
            font-size: 0.8rem;
            color: #666;
            padding: 0.5rem;
            background: #f8f9fa;
            border-radius: 4px;
            margin: 0.5rem 0;
        }
        .user-email {
            color: #424242;
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=True):
        st.markdown('<div class="form-header"><h1>🔑 Welcome Back!</h1></div>', unsafe_allow_html=True)
        st.markdown('<div class="form-subheader">Please sign in with your email address</div>', unsafe_allow_html=True)
        
        email = st.text_input("Email Address", placeholder="Enter your email address")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("Sign In", use_container_width=True)
        
        if submit:
            if not email or not password:
                st.error("Please enter both email and password")
            else:
                success, message = cognito_auth.sign_in(email, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

def show_registration_form():
    if 'registration_step' not in st.session_state:
        st.session_state.registration_step = 'register'
        st.session_state.registered_email = None

    if st.session_state.registration_step == 'register':
        with st.form("register_form", clear_on_submit=True):
            st.markdown('<div class="form-header"><h1>📝 Create Account</h1></div>', unsafe_allow_html=True)
            st.markdown('<div class="form-subheader">Join AutoEDA to start analyzing your data</div>', unsafe_allow_html=True)
            
            email = st.text_input("Email Address", placeholder="Enter your email address")
            
            st.markdown('<div class="password-requirements">Password must contain:<br>• At least 8 characters<br>• At least one uppercase letter<br>• At least one lowercase letter<br>• At least one number<br>• At least one special character</div>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            submit = st.form_submit_button("Create Account", use_container_width=True)
            
            if submit:
                if not all([email, password, confirm_password]):
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    success, message = cognito_auth.sign_up(email, password, email)
                    if success:
                        st.success(message)
                        st.session_state.registration_step = 'verify'
                        st.session_state.registered_email = email
                        st.rerun()
                    else:
                        st.error(message)
    
    elif st.session_state.registration_step == 'verify':
        with st.form("verification_form"):
            st.markdown('<div class="form-header"><h2>✉️ Verify Your Email</h2></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="form-subheader">A verification code has been sent to {st.session_state.registered_email}</div>', unsafe_allow_html=True)
            
            verification_code = st.text_input("Verification Code", placeholder="Enter the 6-digit code")
            submit = st.form_submit_button("Verify Email", use_container_width=True)
            
            if submit:
                if not verification_code:
                    st.error("Please enter the verification code")
                else:
                    success, message = cognito_auth.confirm_sign_up(st.session_state.registered_email, verification_code)
                    if success:
                        st.success(message)
                        st.info("You can now sign in with your email and password")
                        # Reset registration step
                        st.session_state.registration_step = 'register'
                        st.session_state.registered_email = None
                        # Switch to login tab
                        st.session_state.active_tab = 0
                        st.rerun()
                    else:
                        st.error(message)

        if st.button("← Back to Registration", use_container_width=True):
            st.session_state.registration_step = 'register'
            st.session_state.registered_email = None
            st.rerun()

def show_password_reset():
    if 'reset_step' not in st.session_state:
        st.session_state.reset_step = 'request'
        st.session_state.reset_email = None

    if st.session_state.reset_step == 'request':
        with st.form("reset_password_form"):
            st.markdown('<div class="form-header"><h1>🔒 Reset Password</h1></div>', unsafe_allow_html=True)
            st.markdown('<div class="form-subheader">Enter your email address to receive a reset code</div>', unsafe_allow_html=True)
            
            email = st.text_input("Email Address", placeholder="Enter your email address")
            submit = st.form_submit_button("Send Reset Code", use_container_width=True)
            
            if submit:
                if not email:
                    st.error("Please enter your email address")
                else:
                    success, message = cognito_auth.reset_password(email)
                    if success:
                        st.success(message)
                        st.session_state.reset_step = 'confirm'
                        st.session_state.reset_email = email
                        st.rerun()
                    else:
                        st.error(message)
    
    elif st.session_state.reset_step == 'confirm':
        with st.form("reset_password_confirmation_form"):
            st.markdown('<div class="form-header"><h2>🔐 Set New Password</h2></div>', unsafe_allow_html=True)
            
            verification_code = st.text_input("Reset Code", placeholder="Enter the code from your email")
            
            st.markdown('<div class="password-requirements">Password must contain:<br>• At least 8 characters<br>• At least one uppercase letter<br>• At least one lowercase letter<br>• At least one number<br>• At least one special character</div>', unsafe_allow_html=True)
            new_password = st.text_input("New Password", type="password", placeholder="Create a new password")
            confirm_password = st.text_input("Confirm New Password", type="password", placeholder="Confirm your new password")
            
            submit = st.form_submit_button("Reset Password", use_container_width=True)
            
            if submit:
                if not all([verification_code, new_password, confirm_password]):
                    st.error("Please fill in all fields")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    success, message = cognito_auth.confirm_reset_password(st.session_state.reset_email, verification_code, new_password)
                    if success:
                        st.success(message)
                        st.info("You can now sign in with your new password")
                        # Reset password reset step
                        st.session_state.reset_step = 'request'
                        st.session_state.reset_email = None
                        # Switch to login tab
                        st.session_state.active_tab = 0
                        st.rerun()
                    else:
                        st.error(message)

        if st.button("← Back to Reset Password", use_container_width=True):
            st.session_state.reset_step = 'request'
            st.session_state.reset_email = None
            st.rerun()

def show_logout_button():
    # Display user email in the sidebar
    if 'user_email' in st.session_state:
        st.sidebar.markdown(f'<p class="user-email">Welcome, {st.session_state.user_email}</p>', unsafe_allow_html=True)
    
    if st.sidebar.button("Sign Out"):
        success, message = cognito_auth.sign_out()
        if success:
            st.success(message)
            # Clear session state
            for key in ['authenticated', 'user_email', 'id_token', 'access_token', 'refresh_token']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        else:
            st.error(message)

def check_auth():
    # Check if token needs refresh
    if st.session_state.get('authenticated', False):
        if not cognito_auth.is_token_valid():
            success, message = cognito_auth.refresh_token()
            if not success:
                st.warning("Session expired. Please sign in again.")
                st.session_state.authenticated = False
                return False
    
    if not st.session_state.get('authenticated', False):
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["🔑 Sign In", "📝 Create Account", "🔒 Reset Password"])
        
        # Sign In Tab
        with tab1:
            show_login_page()
        
        # Create Account Tab
        with tab2:
            show_registration_form()
        
        # Reset Password Tab
        with tab3:
            show_password_reset()
        
        return False
    return True 