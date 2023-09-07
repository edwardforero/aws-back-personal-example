import boto3


def query_autocomplete_limit(table_name, params):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = None
    items = []
    limit = params['Limit'] = int(params.get('Limit', 25))
    control_limit = 10
    while response is None or (len(response.get('LastEvaluatedKey', {})) > 0 and len(items) < limit):
        if response is not None and 'LastEvaluatedKey' in response:
            if limit > 0:
                params['Limit'] = limit - len(items)
            params['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = table.query(**params)
        items += response.get('Items', []) 
        control_limit -= 1
        if limit <= 0 and control_limit <= 0:
            break
            
    return {
        'LastEvaluatedKey': response.get('LastEvaluatedKey'),
        'Items': items,
    }