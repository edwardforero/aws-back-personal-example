import os

import boto3
import cfnresponse


def lambda_handler(event, context):
    response_code = 200
    try:
        api_gateway_client = boto3.client('apigateway')
        api_key_id = event['ResourceProperties']['ApiKeyID']
        response = api_gateway_client.get_api_key(
            apiKey=api_key_id,
            includeValue=True
        )
        data = """
#.env file
REACT_APP_BUCKET=
REACT_APP_BUCKET_URL=
MAX_ATTACHMENT_SIZE=5000000
REACT_APP_TITLE={SITE_NAME}
REACT_APP_REGION={REGION}
REACT_APP_API_NAME={API_NAME}
REACT_APP_USER_POOL_ID={USER_POOL_ID}
REACT_APP_APP_CLIENT_ID={APP_CLIENT_ID}
REACT_APP_IDENTITY_POOL_ID={IDENTITY_POOL_ID}
REACT_APP_API_URL={API_URL}
REACT_APP_API_KEY={API_KEY}
        """.format(**os.environ, API_KEY=response['value'])
        responseData = {
            'Data': data,
        }
    except Exception as e:
        print(e)
        print(event)
        responseData = {
            'Data': 'Lambda Error',
        }
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, "CustomResourcePhysicalID", noEcho=True)