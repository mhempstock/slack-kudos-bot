from aws_lambda_powertools import Logger, Tracer # type: ignore
from src.handlers.events_handler import handle_message
from src.handlers.commands_handler import handle_slash_command
import json
import urllib
import os

# --- Global Constants ---
VERIFICATION_TOKEN = os.environ.get('VERIFICATION_TOKEN')

logger = Logger()
tracer = Tracer()

def verify_token(body):
    """
    Verifies the token from the incoming Slack request.
    """
    token = body.get('token')
    if token != VERIFICATION_TOKEN:
        logger.error("Invalid Verification Token")
        return False
    return True

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler_events(event, context):
    if event.get("body"):
        body = json.loads(event["body"])

        # --- Verify Token First ---
        if not verify_token(body):
            return {
                "statusCode": 403,
                "body": json.dumps({"message": "Forbidden"})
            }

        # --- Handle Slack URL Verification Challenge ---
        if body.get("type") == "url_verification":
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "text/plain"},
                "body": body["challenge"]
            }

        # --- Process the Event ---
        handle_message(body)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Event processed"})
    }

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler_commands(event, context):
    if event.get("body"):
        body = dict(urllib.parse.parse_qsl(event["body"]))

        # --- Verify Token First ---
        if not verify_token(body):
            return {
                "statusCode": 403,
                "body": json.dumps({"message": "Forbidden"})
            }

        # --- Process the Slash Command ---
        message = handle_slash_command(body)
    if message:
        return {
            "statusCode": 200,
            "body":  message
            }
    else:
        return {
            "statusCode": 200,
            "body": "",
            "headers": {
                "Content-Type": "application/json"
            }
        }