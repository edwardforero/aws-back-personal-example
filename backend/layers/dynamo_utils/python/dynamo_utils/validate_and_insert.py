import boto3
from typing import Union

from utils.custom_exception import CustomException

from .validate_model import validate_model
from .models.my_base_model import MyBaseModel


def validate_and_insert(table_name: str, my_model: MyBaseModel, data: Union[str, map]):
    dynamodb = boto3.resource('dynamodb')
    model_data = validate_model(my_model, data)
    # model_data.set_default_insert_values()
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key=model_data.get_key(),
        # ProjectionExpression='contact.phone'
    )
    if response.get('Item', None) is not None:
        raise CustomException(400, "An Item with the same ID already exists.")
    dict_data = model_data.dict(exclude_none=True) # exclude_unset=True)
    table.put_item(Item=dict_data)
    return dict_data
