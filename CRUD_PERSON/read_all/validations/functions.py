import json


def validate_connection(conn):
    if conn is None:
        return {"statusCode": 500, "body": json.dumps({"error": "Connection not provided."})}
    return None
