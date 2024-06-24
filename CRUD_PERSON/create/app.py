import json
import psycopg2
from validations.functions import validate_connection, validate_event_body, validation_payload


def lambda_handler(event, _context):
    global conn
    try:
        # Database connection
        conn = connection_db_postgres(
            host='ep-gentle-mode-a4hjun6w-pooler.us-east-1.aws.neon.tech',
            user='default',
            password='pnQI1h7sNfFK',
            database='verceldb'
        )

        # Validate connection
        valid_conn_res = validate_connection(conn)
        if valid_conn_res is not None:
            return valid_conn_res

        # Validate body in event
        valid_event_body_res = validate_event_body(event)
        if valid_event_body_res is not None:
            return valid_event_body_res

        # Validate payload
        request_body = json.loads(event['body'])
        valid_payload_res = validation_payload(request_body)
        if valid_payload_res is not None:
            return valid_payload_res

        # Get payload values
        name = request_body['name']
        age = request_body['age']

        # create transaction
        query = """ INSERT INTO recu_people (name, age) VALUES (%s, %s) RETURNING id """
        values = (name, age)

        result = transaction_db(conn, query, values)

        return {"statusCode": 200, "body": json.dumps({"data": "Person created successfully", "id": result[0][0]})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
    finally:
        conn.close()


def connection_db_postgres(host, user, password, database):
    conn_db = psycopg2.connect(host=host, user=user, password=password, database=database)
    return conn_db


def transaction_db(conn_db, query, values):
    cur = conn_db.cursor()
    conn_db.autocommit = False

    cur.execute(query, values)

    if query.split()[0].lower() == 'select':
        result = cur.fetchall()
    else:
        result = cur.rowcount

    conn_db.commit()
    cur.close()

    return result
