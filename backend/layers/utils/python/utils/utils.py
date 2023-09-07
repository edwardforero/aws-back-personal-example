import base64
from datetime import datetime, timedelta
from decimal import Decimal
import json
from os import environ, path
import random
import re
import string
import time

from boto3 import resource


def save_errors(lambda_name, error, data = {}, trace = None):
    item_table = resource('dynamodb').Table(environ["table_errors"])
    ttl = (datetime.utcnow() + timedelta(7)).timestamp()
    item_table.put_item(Item={
        'lambdaName': lambda_name,
        'timestampCreated': datetime.utcnow().isoformat(),
        'error': error,
        'trace': trace,
        'inputData': json.dumps(data, cls=CustomJsonEncoder),
        'ttl': Decimal(ttl),
    })

class CustomJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            # return obj.isoformat()
            return obj.isoformat()
        return super(CustomJsonEncoder, self).default(obj)

def default_response(status_code, response):
    return {
        "statusCode": status_code,
        "body": json.dumps(response, cls=CustomJsonEncoder) \
                    if response is not None and type(response) != str 
                    else response,
        "headers": {
            "Accept-Language": "",
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Token": "",
            "X-Api-Key": "" ,
        },
    }

def get_b64_id():
    return base64.b32encode(time.time_ns().to_bytes(8, byteorder='big')) \
                            .decode('utf-8').rstrip('=')

def remove_accents(string):
    new = string.lower()
    new = re.sub(r'[àáâãäå]', 'a', new)
    new = re.sub(r'[èéêë]', 'e', new)
    new = re.sub(r'[ìíîï]', 'i', new)
    new = re.sub(r'[òóôõö]', 'o', new)
    new = re.sub(r'[ùúûü]', 'u', new)
    return new

def clean_special_chars(string, remove_space=False):
    if remove_space is False:
        regex = '[^A-Za-z0-9 _]+'
    else:
        regex = '[^A-Za-z0-9]+'
    return re.sub(regex, '', remove_accents(string))

def search_dict_path(p_dict: dict, p_path: str):
    if type(p_dict) != dict or type(p_path) != str:
        raise Exception("Invalid params type")
    path_list = p_path.split(".")
    tmp_value = p_dict
    for x in range(len(path_list)):
        if path_list[x] in tmp_value:
            tmp_value = tmp_value[path_list[x]]
        else:
            return None
    return tmp_value

def clean_and_validate_email(email):
    script_dir = path.dirname(path.abspath(__file__))
    file_path = path.join(script_dir, 'valid_domains.json')
    json_file = open(file_path, 'r')
    list_of_valids_domains = json.load(json_file)
    email_parts = email.lower().split("@")
    email_prefix = email_parts[0]
    domain = email_parts[-1]
    if len(email_parts) != 2 or domain not in list_of_valids_domains:
        raise Exception("Ivalid email")
    final_email = email_prefix.split("+")[0] + f"@{domain}"
    return final_email


def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def has_seller_access(token_data, seller_id):
    sellers = json.loads(token_data.get('owned_sellers', '[]'))\
                 + json.loads(token_data.get('maintainable_sellers', '[]')) 
    role = token_data.get('custom:role', '')
    return role == "admin" or (role == "seller" and seller_id in sellers)

def my_decimal(value):
    return Decimal(value).quantize(Decimal('.01'))

