import boto3
import os

import jwt

from utils.default_middleware import default_middleware
from utils.custom_exception import CustomException

@default_middleware
def lambda_handler(event, context):
    if "email" not in event['body'] or "password" not in event['body']:
        raise CustomException(400, "email and password are required")
    resp = get_cognito_auth_token(event['body'])
    if resp['token_data'].get('custom:role') not in ['admin', 'seller']:
        raise CustomException(403, "invalid role")

    return {"status_code": 200, "response": resp}

def get_cognito_auth_token(data):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        ClientId=os.environ['CLIENT_ID'],
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': data['email'],
            'PASSWORD': data['password'],
        },
    )
    if 'AuthenticationResult' not in response:
        raise CustomException(403, "invalid user status")
    access_token = response['AuthenticationResult']['IdToken']

    response = {
        'token_data': jwt.decode(access_token, options={"verify_signature": False}),
        'token': access_token,
    }
    # print(f'Id Token: {access_token}')
    # return access_token
    return response



