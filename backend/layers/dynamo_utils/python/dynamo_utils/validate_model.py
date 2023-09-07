from typing import Union
from pydantic import BaseModel, ValidationError

from utils.custom_exception import CustomException

def validate_model(my_model: BaseModel, data: Union[str, map]):
    try:
        if type(data) == str:
            model_instance = my_model.parse_raw(data)
        else:
            model_instance = my_model.parse_obj(data)

        return model_instance
    except ValidationError as e:
        raise CustomException(400, e.json())


