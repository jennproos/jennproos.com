import boto3
import botocore
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel("INFO")
my_email = os.environ["MY_EMAIL"]
ses_client = boto3.client("ses")

def handler(event, context):
    body = json.loads(event["body"])
    logger.info(f"event body: {body}")

    first_name = body["firstName"]
    last_name = body["lastName"]
    email = body["email"]
    phone = body["phone"]
    message = body["message"]

    message_body = f"""{first_name} {last_name} has sent you a message:\n
    {message}\n\n
    Contact info:\n
    E-mail: {email}\n
    Phone: {phone}\n"""

    try:
        response = ses_client.send_email(
            Source=my_email,
            Destination={
                "ToAddresses": ["jennproos@gmail.com"]
            },
            Message={
                "Subject": {
                    "Data": f"Message from {first_name} {last_name}",
                    "Charset": "utf-8"
                },
                "Body": {
                    "Text": {
                        "Data": message_body,
                        "Charset": "utf-8"
                    }
                }
            }
        )
        message_id = response["MessageId"]
        logger.info(f"Successfully sent e-mail with MessageId {message_id}")

    except botocore.exceptions.ClientError as error:
        logger.error(f"Error caught trying to send e-mail: {error}")
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            }
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        }
    }