import boto3
import datetime
import json
import os
import re
from .utils import get_b64_id

from .media_file import validate_media_file_extension, CONFIG_FILES
from .custom_exception import CustomException

FILE_KEY_PATTERN = r"^sellers/([a-z][a-z0-9-]+)/([a-z0-9-_]+)/(?:media-id/[a-zA-Z0-9]+/)?([a-zA-Z0-9-_]+)\.([a-zA-Z0-9]{2,4})$"


def generate_media_file_path(seller_id, media_type, extension):
    
    validation = validate_media_file_extension(media_type, extension)
    if validation['isValid'] is False:
        raise CustomException(400, "invalid media file extension, valid extension are: " + (", ".join(validation['valids'])))
    if media_type in CONFIG_FILES:
        return f"sellers/{seller_id}/config/{media_type}.{extension}"
    return f"sellers/{seller_id}/{media_type}/{get_b64_id()}.{extension}"

def generate_stripe_payment_path(payment_type, seller_id, username, event_name, id_payment=get_b64_id()):
    date_path = datetime.datetime.now().strftime("%Y-%m-%d")
    return f"stripe/{payment_type}/{event_name}/sellers/{seller_id}/username/{username}/{date_path}-{id_payment}.json"

def generate_media_file_prefix(seller_id, media_type, media_id ):
    # media_id = get_b64_id()
    return f"sellers/{seller_id}/{media_type}/media-id/{media_id}/"

def get_media_file_id_from_path(path):
    return path.split("media-id/")[-1].split("/")[0]

def validate_media_file_from_s3(bucket_name, file_key, media_type):

    validation = validate_media_file_extension(media_type, file_key)
    if validation['isValid'] is False:
        raise CustomException(400, "invalid media file extension, valid extension are: " + (", ".join(validation['valids'])))
    if re.match(FILE_KEY_PATTERN, file_key) is None:
        raise CustomException(400, f"invalid media file path, pattern required: {FILE_KEY_PATTERN}")
    try:
        s3_resource = boto3.resource("s3")
        bucket = s3_resource.Bucket(name=bucket_name)
        return bucket.Object(key=file_key)
    except Exception as e:
        print(e)
        raise CustomException(400, "File doesn't not exists.")

def save_stripe_payment_data(payment_type, payment_data, seller_id, username, event_name, id_payment):
    json_data = json.dumps(payment_data)
    s3 = boto3.client('s3')
    file_key = generate_stripe_payment_path(payment_type, seller_id, username, event_name, id_payment)
    s3.put_object(Body=json_data, Bucket=os.environ['s3_media_files'], Key=file_key)
    return file_key