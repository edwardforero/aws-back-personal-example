import json
import traceback

from .utils import default_response, save_errors
from .custom_exception import CustomException

def default_middleware(handler):
    def wrapper(event, context):
        print("default_middleware - starting")
        lambda_name = context.function_name
        try:
            event['body'] = json.loads(event['body']) if event.get('body', None) is not None else {}
            result = handler(event, context)
            print("default_middleware - finishing")
            return default_response(result.get('status_code', 400), result.get('response', None))
        
        except CustomException as e:
            print(e)
            if e.save_error is True:
                save_errors(lambda_name, e.message, event)
            return default_response(e.status_code, e.message)

        except Exception as e:
            print(e)
            traceback.print_exc()
            trace = traceback.format_exc()
            save_errors(lambda_name, str(e), event, trace)
            return default_response(500, str(e))

    return wrapper
