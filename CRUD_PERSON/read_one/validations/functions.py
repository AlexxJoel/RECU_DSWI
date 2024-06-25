import json
import re

# REGEX
letters_regex = re.compile(r"^[a-zA-Z\s]+$")
date_regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")
phoneNumber_regex = re.compile(r"^\+?[1-9]\d{1,14}|\(\d{1,4}\)\s*\d{1,4}(-|\s)?\d{1,4}$")
email_regex = (r"^\[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def validate_connection(conn):
    if conn is None:
        return {"statusCode": 500, "body": json.dumps({"error": "Connection not provided."})}
    return None


def validate_event_path_params(event):
    if "pathParameters" not in event:
        return {"statusCode": 400, "body": json.dumps({"error": "Path parameters is missing from the request."})}

    if not event["pathParameters"]:
        return {"statusCode": 400, "body": json.dumps({"error": "Path parameters is null."})}


def validate_id(value):
    if value <= 0:
        return {"statusCode": 400, "body": json.dumps({"error": "Request ID invalid value."})}
    return None
