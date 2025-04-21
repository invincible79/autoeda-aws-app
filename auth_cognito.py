import boto3
import os
import streamlit as st
from botocore.exceptions import ClientError
import json
from datetime import datetime, timedelta
import jwt
import hmac
import hashlib
import base64
from config import cognito_client, COGNITO_USER_POOL_ID, COGNITO_CLIENT_ID

class CognitoAuth:
    def __init__(self):
        self.user_pool_id = COGNITO_USER_POOL_ID
        self.client_id = COGNITO_CLIENT_ID
        self.client_secret = os.getenv('COGNITO_CLIENT_SECRET')
        self.region = 'ap-south-1'
        self.issuer = f'https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}'
    
    def get_secret_hash(self, username):
        """Calculate the secret hash for Cognito API calls"""
        message = username + self.client_id
        dig = hmac.new(
            str(self.client_secret).encode('utf-8'),
            msg=str(message).encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode()
        
    def sign_up(self, username, password, email):
        try:
            secret_hash = self.get_secret_hash(username)
            response = cognito_client.sign_up(
                ClientId=self.client_id,
                SecretHash=secret_hash,
                Username=username,
                Password=password,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email
                    }
                ]
            )
            return True, "Please check your email for verification code"
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'UsernameExistsException':
                return False, "Username already exists"
            elif error_code == 'InvalidPasswordException':
                return False, "Password does not meet requirements"
            else:
                return False, str(e)

    def confirm_sign_up(self, username, confirmation_code):
        try:
            secret_hash = self.get_secret_hash(username)
            cognito_client.confirm_sign_up(
                ClientId=self.client_id,
                SecretHash=secret_hash,
                Username=username,
                ConfirmationCode=confirmation_code
            )
            return True, "Account confirmed successfully"
        except ClientError as e:
            return False, str(e)

    def sign_in(self, username, password):
        try:
            secret_hash = self.get_secret_hash(username)
            response = cognito_client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password,
                    'SECRET_HASH': secret_hash
                }
            )
            
            # Store tokens in session state
            auth_result = response['AuthenticationResult']
            st.session_state.id_token = auth_result['IdToken']
            st.session_state.access_token = auth_result['AccessToken']
            st.session_state.refresh_token = auth_result['RefreshToken']
            st.session_state.token_expiry = datetime.now() + timedelta(seconds=auth_result['ExpiresIn'])
            st.session_state.username = username
            
            return True, "Successfully signed in"
        except ClientError as e:
            error = e.response['Error']
            return False, f"An error occurred ({error['Code']}): {error['Message']}"

    def refresh_token(self):
        if 'refresh_token' not in st.session_state:
            return False, "No refresh token available"
            
        try:
            secret_hash = self.get_secret_hash(st.session_state.username)
            response = cognito_client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': st.session_state.refresh_token,
                    'SECRET_HASH': secret_hash
                }
            )
            
            # Update tokens in session state
            auth_result = response['AuthenticationResult']
            st.session_state.id_token = auth_result['IdToken']
            st.session_state.access_token = auth_result['AccessToken']
            st.session_state.token_expiry = datetime.now() + timedelta(seconds=auth_result['ExpiresIn'])
            
            return True, "Token refreshed successfully"
        except ClientError as e:
            error = e.response['Error']
            return False, f"An error occurred ({error['Code']}): {error['Message']}"

    def sign_out(self):
        try:
            if 'access_token' in st.session_state:
                cognito_client.global_sign_out(
                    AccessToken=st.session_state['access_token']
                )
            
            # Clear session state
            for key in ['id_token', 'access_token', 'refresh_token', 'token_expiry', 'username', 'authenticated']:
                if key in st.session_state:
                    del st.session_state[key]
            
            return True, "Logged out successfully"
        except ClientError as e:
            return False, str(e)

    def is_token_valid(self):
        return ('token_expiry' in st.session_state and 
                datetime.now() < st.session_state.token_expiry)

    def get_user_info(self):
        if not self.is_token_valid():
            if 'refresh_token' in st.session_state:
                success, message = self.refresh_token()
                if not success:
                    return None
            else:
                return None
                
        try:
            response = cognito_client.get_user(
                AccessToken=st.session_state['access_token']
            )
            return response
        except ClientError:
            return None

    def reset_password(self, username):
        try:
            secret_hash = self.get_secret_hash(username)
            cognito_client.forgot_password(
                ClientId=self.client_id,
                SecretHash=secret_hash,
                Username=username
            )
            return True, "Password reset code sent to your email"
        except ClientError as e:
            return False, str(e)

    def confirm_reset_password(self, username, confirmation_code, new_password):
        try:
            secret_hash = self.get_secret_hash(username)
            cognito_client.confirm_forgot_password(
                ClientId=self.client_id,
                SecretHash=secret_hash,
                Username=username,
                ConfirmationCode=confirmation_code,
                Password=new_password
            )
            return True, "Password reset successful"
        except ClientError as e:
            return False, str(e)

# Initialize CognitoAuth instance
cognito_auth = CognitoAuth() 