import boto3
from typing import Union

from utils.custom_exception import CustomException

from .validate_model import validate_model
from .models.my_base_model import MyBaseModelUpdate



def generate_dynamo_update_dict(model_data: MyBaseModelUpdate, old_data: dict):
    non_updatable = model_data.get_non_updatable_fields()
    new_data = model_data.dict(exclude_none=True) # exclude_unset=True
    dynamo_data = {
        'ExpressionAttributeNames': {},
        'ExpressionAttributeValues': {},
    }
    update_expression = []
    fields_valids_to_update = 0
    not_countable_fields = model_data.get_not_countable_fields()
    for key in new_data:
        valid_field = new_data[key] != None and key not in non_updatable
        if valid_field and (old_data.get(key, None) != new_data[key] or key in not_countable_fields):
            dynamo_data['ExpressionAttributeNames']['#%s' % key] = key
            dynamo_data['ExpressionAttributeValues'][':%s' % key] = new_data[key]
            update_expression.append("#{key}=:{key}".format(key=key))
            if key not in not_countable_fields:
                fields_valids_to_update += 1
    
    if fields_valids_to_update == 0:
        print(dynamo_data['ExpressionAttributeNames'])
        raise CustomException(400, 'Without new information to update')
    dynamo_data['UpdateExpression'] = 'SET ' + (', '.join(update_expression))
    return dynamo_data

def validate_and_update(table_name: str, my_model: MyBaseModelUpdate, data: Union[str, map]):
    dynamodb = boto3.resource('dynamodb')
    model_data = validate_model(my_model, data)
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key=model_data.get_key(),
    )
    old_data = response.get('Item', None)
    if old_data is None:
        raise CustomException(400, "Item does not exists")
        
    dynamo_data = generate_dynamo_update_dict(model_data, old_data)
    result = table.update_item(
        Key=model_data.get_key(),
        ReturnValues='ALL_NEW',
        **dynamo_data,
    )['Attributes']
    return  my_model.parse_obj(result)

def update_item(table_name: str, my_model: MyBaseModelUpdate, data: map):
    model_data = validate_model(my_model, data)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    dynamo_data = generate_dynamo_update_dict(model_data, {})
    result = table.update_item(
        Key=model_data.get_key(),
        ReturnValues='ALL_NEW',
        **dynamo_data,
    )['Attributes']
    return  my_model.parse_obj(result)