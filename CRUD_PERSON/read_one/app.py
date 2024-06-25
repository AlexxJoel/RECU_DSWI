import json
import psycopg2
from psycopg2.extras import RealDictCursor
from validations.functions import validate_connection, validate_event_path_params, validate_id


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

        # Validate params
        valid_event_path = validate_event_path_params(event)
        if valid_event_path is not None:
            return valid_event_path

        valid_id = validate_id(event)
        if valid_id is not None:
            return valid_id

        # Get values from path params
        id = event['pathParameters']['id']
        # create transaction
        query = """ SELECT * FROM recu_people WHERE id = %s """

        result = transaction_db(conn, query, (id,))

        if not result:
            return {"statusCode": 204, "body": json.dumps({"error": "Person not found"})}

        return {"statusCode": 200, "body": json.dumps({"data": "Person created successfully", "result": result})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
    finally:
        conn.close()


def connection_db_postgres(host, user, password, database):
    conn_db = psycopg2.connect(host=host, user=user, password=password, database=database)
    return conn_db


def transaction_db(conn_db, query, values):
    cur = conn_db.cursor(cursor_factory=RealDictCursor)
    cur.execute(query, values)
    result = cur.fetchone()
    conn_db.commit()
    cur.close()

    return result
