import boto3
from typing import List, Type
from pydantic import BaseModel, validator
import traceback

from .validate_model import validate_model
from .models.my_base_model import MyBaseModel
# from .models.political_division_model import PoliticalDivisionModel

BATCH_SIZE = 25


class BatchInsertData(BaseModel):
    table_name: str
    model: Type[MyBaseModel]
    items: List
    stop_all_on_any_row_error: bool = False
    
    # valida que el ID del usuario tenga un valor
    @validator('table_name')
    def user_id_must_not_be_empty(cls, value):
        if not value or len(value) < 4:
            raise ValueError('user_id must not be empty')
        return value

def batch_insert(insertData: BatchInsertData):
    if type(insertData) != BatchInsertData:
        raise Exception("input data must be of type BatchInsertData")
    errors = []
    grouped_ids = []
    group_items = []
    for i in range(len(insertData.items)):
        try:
            item_data = validate_model(insertData.model, insertData.items[i])
            keys = item_data.get_key()
            if keys in grouped_ids:
                errors.append(f"Error on row {i}, ids already exists: {keys}")
                continue
            grouped_ids.append(keys)
            group_items.append(item_data.dict(exclude_none=True))
        except Exception as e:
            traceback.print_exc()
            print(f"Error on row {i}, error: {e}")
            errors.append(f"Error on row {i}, error: {e}")
    if insertData.stop_all_on_any_row_error == True and len(errors) > 0:
        raise Exception(errors)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(insertData.table_name)
    with table.batch_writer() as batch:
        for i in range(len(group_items)):
            batch.put_item(
                Item=group_items[i]
            )
