

FREE_SALES = ["free"]
MEMBERSHIP_OPTION = "only-membership"
PAYMENT_OPTION = "only-payment"
MEMBERSHIP_AND_PAYMENT_OPTION = "membership-and-payment"
KIND_OF_SALE = FREE_SALES + [MEMBERSHIP_OPTION, PAYMENT_OPTION, MEMBERSHIP_AND_PAYMENT_OPTION]

def validate_type_of_sale(type_of_sale):
    return {"isValid": type_of_sale in KIND_OF_SALE, "valids": KIND_OF_SALE}


def validate_type_of_sale_requirements(type_of_sale, params):
    is_valid = True
    msg = ""
    if type_of_sale in (MEMBERSHIP_OPTION, MEMBERSHIP_AND_PAYMENT_OPTION):
        membership_required = params.get("minimumMembershipRequired", "")
        if membership_required in (None, "") or membership_required < 1:
            msg = "The minimumMembershipRequired field is mandatory and must be greater than zero. "
            is_valid = False

    if type_of_sale in (PAYMENT_OPTION, MEMBERSHIP_AND_PAYMENT_OPTION):
        price = params.get("price", "")
        if price in (None, "", 0) or price <= 0:
            is_valid = False
            msg = "The price field is mandatory and must be greater than zero."
    
    return {"isValid": is_valid , "msg": msg}
        