import boto3
import os
from config import cognito_client, AWS_REGION

def create_user_pool():
    """Create a Cognito User Pool"""
    try:
        response = cognito_client.create_user_pool(
            PoolName='AutoEDAUserPool',
            Policies={
                'PasswordPolicy': {
                    'MinimumLength': 8,
                    'RequireUppercase': True,
                    'RequireLowercase': True,
                    'RequireNumbers': True,
                    'RequireSymbols': True
                }
            },
            AutoVerifiedAttributes=['email'],
            Schema=[
                {
                    'Name': 'email',
                    'AttributeDataType': 'String',
                    'Required': True,
                    'Mutable': True
                },
                {
                    'Name': 'name',
                    'AttributeDataType': 'String',
                    'Required': True,
                    'Mutable': True
                }
            ],
            MfaConfiguration='OFF',
            UserPoolTags={
                'Project': 'AutoEDA'
            }
        )
        return response['UserPool']['Id']
    except Exception as e:
        print(f"Error creating user pool: {str(e)}")
        return None

def create_app_client(user_pool_id):
    """Create an app client for the user pool"""
    try:
        response = cognito_client.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName='AutoEDAWebClient',
            GenerateSecret=True,
            RefreshTokenValidity=30,
            AccessTokenValidity=60,
            IdTokenValidity=60,
            TokenValidityUnits={
                'AccessToken': 'minutes',
                'IdToken': 'minutes',
                'RefreshToken': 'days'
            },
            ReadAttributes=[
                'email',
                'name',
                'email_verified'
            ],
            WriteAttributes=[
                'email',
                'name'
            ],
            ExplicitAuthFlows=[
                'ALLOW_USER_PASSWORD_AUTH',
                'ALLOW_REFRESH_TOKEN_AUTH'
            ],
            PreventUserExistenceErrors='ENABLED'
        )
        return response['UserPoolClient']['ClientId']
    except Exception as e:
        print(f"Error creating app client: {str(e)}")
        return None

def create_identity_pool(user_pool_id, client_id):
    """Create an identity pool"""
    try:
        cognito_identity = boto3.client('cognito-identity', region_name=AWS_REGION)
        response = cognito_identity.create_identity_pool(
            IdentityPoolName='AutoEDAIdentityPool',
            AllowUnauthenticatedIdentities=False,
            CognitoIdentityProviders=[
                {
                    'ProviderName': f'cognito-idp.{AWS_REGION}.amazonaws.com/{user_pool_id}',
                    'ClientId': client_id,
                    'ServerSideTokenCheck': True
                }
            ]
        )
        return response['IdentityPoolId']
    except Exception as e:
        print(f"Error creating identity pool: {str(e)}")
        return None

def setup_cognito():
    """Main function to set up Cognito"""
    print("Setting up Cognito...")
    
    # Create User Pool
    user_pool_id = create_user_pool()
    if not user_pool_id:
        print("Failed to create user pool")
        return
    
    print(f"Created User Pool with ID: {user_pool_id}")
    
    # Create App Client
    client_id = create_app_client(user_pool_id)
    if not client_id:
        print("Failed to create app client")
        return
    
    print(f"Created App Client with ID: {client_id}")
    
    # Create Identity Pool
    identity_pool_id = create_identity_pool(user_pool_id, client_id)
    if not identity_pool_id:
        print("Failed to create identity pool")
        return
    
    print(f"Created Identity Pool with ID: {identity_pool_id}")
    
    # Save configuration
    with open('.env', 'a') as f:
        f.write(f"\nCOGNITO_USER_POOL_ID={user_pool_id}")
        f.write(f"\nCOGNITO_CLIENT_ID={client_id}")
        f.write(f"\nCOGNITO_IDENTITY_POOL_ID={identity_pool_id}")
    
    print("\nCognito setup completed successfully!")
    print("Please update your application configuration with these values:")
    print(f"User Pool ID: {user_pool_id}")
    print(f"Client ID: {client_id}")
    print(f"Identity Pool ID: {identity_pool_id}")

if __name__ == "__main__":
    setup_cognito() 