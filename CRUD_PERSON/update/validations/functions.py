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


def validate_event_body(event):
    if "body" not in event:
        return {"statusCode": 400, "body": json.dumps({"error": "No body provided."})}

    if event["body"] is None:
        return {"statusCode": 400, "body": json.dumps({"error": "Body is null."})}

    if not event["body"]:
        return {"statusCode": 400, "body": json.dumps({"error": "Body is empty."})}

    if isinstance(event["body"], list):
        return {"statusCode": 400, "body": json.dumps({"error": "Body can not be a list."})}

    try:
        json.loads(event['body'])
    except json.JSONDecodeError:
        return {"statusCode": 400, "body": json.dumps({"error": "The request body is not valid JSON"})}

    return None


def validate_id(payload):
    if "id" not in payload or not isinstance(payload["id"], int):
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid or missing 'id'"})}

    if payload["id"] <= 0:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid 'id' format"})}
    return None


def validation_payload(payload):
    # check first required fields
    if ("name" not in payload or not isinstance(payload["name"], str) or
            "age" not in payload or not isinstance(payload["age"], int)):
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid or missing 'name' or 'age'"})}

    # check format of fields
    if not letters_regex.match(payload["name"]):
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid 'name' format"})}

    if payload["age"] < 0:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid 'age' format"})}

    # check optional fields
    if "email" in payload and not email_regex.match(payload["email"]):
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid 'email' format"})}

    return None
