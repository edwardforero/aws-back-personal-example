

def add_aditional_filter_expression(params, name, value, condition='=', valueTwo = None):
    if 'ExpressionAttributeNames' not in params:
        params['ExpressionAttributeNames'] = {}
    if 'ExpressionAttributeValues' not in params:
        params['ExpressionAttributeValues'] = {}
    if 'FilterExpression' in params:
        params['FilterExpression'] += ' and '
    else:
        params['FilterExpression'] = ''

    newName = name.replace('.', '')
    params['ExpressionAttributeNames']['#%s' % newName] = name
    params['ExpressionAttributeValues'][':%s' % newName] = value
    if valueTwo is not None:
        newNameTwo = name.replace('.', '')
        params['ExpressionAttributeValues'][':%sTwo' % newNameTwo] = value

    if condition == 'contains':
        params['FilterExpression'] += 'contains(#{name},:{name})'.format(name=newName)
    elif condition == 'between':
        params['FilterExpression'] += '#{name} >= :{name} AND #{name} <= :{name}Two'.format(name=newName)
    else:
        params['FilterExpression'] += '#{name}{condition}:{name}'.format(name=newName, condition=condition)
