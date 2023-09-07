import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import os

dynamodb = boto3.resource('dynamodb')

USER_ADDITIONAL_DATA = os.environ['table_user_additional_data']

def lambda_handler(event, context):
    user_attributes = event['request']['userAttributes']
    claims_to_add_or_override = get_user_additional_data({}, user_attributes)

    if len(claims_to_add_or_override) > 0:
        event['response']['claimsOverrideDetails'] = {
            'claimsToAddOrOverride': claims_to_add_or_override
        }
    return event


def get_seller_permissions(username):
    params = {
        'KeyConditionExpression': Key('username').eq(username),
        'FilterExpression': Attr('active').eq(True),
    }
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['table_users_rels_sellers'])
    response = table.query(**params)
    items = response.get('Items', [])
    maintainable_sellers = []
    owned_sellers = []
    for x in range(len(items)):
        if items[x]['active'] is False:
            continue
        if items[x]['isOwner'] is False:
            maintainable_sellers.append(items[x]['sellerId'])
        else:
            owned_sellers.append(items[x]['sellerId'])
    return {
        "owned_sellers": json.dumps(owned_sellers),
        "maintainable_sellers": json.dumps(maintainable_sellers),
    }

def get_user_additional_data(claims, user_attributes):
    if user_attributes.get('custom:role') == "admin":
        return claims
    username = user_attributes['email'] if 'email' in user_attributes else \
                user_attributes['phone_number'] if 'phone_number' in user_attributes else user_attributes['sub']
    new_claims = {**claims}
    if user_attributes.get('custom:role') == "seller":
        result = get_seller_permissions(username)
        new_claims['owned_sellers'] = result['owned_sellers']
        new_claims['maintainable_sellers'] = result['maintainable_sellers']
    return new_claims
