from custom_html import prepare_custom_email


def lambda_handler(event, context):
  event = prepare_custom_email(event)
  return event
