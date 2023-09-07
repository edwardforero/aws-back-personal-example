

def add_audit_information(data, token_data):
    name = token_data.get('given_name', 'no name') + ' ' + token_data.get('family_name', '')
    email = token_data.get('email', 'without email')
    return {
        **data,
        "createdBy": f"{email} - {name}",
        "updatedBy": f"{email} - {name}",
    }
    


