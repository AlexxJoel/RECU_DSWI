import json
import psycopg2
from psycopg2.extras import RealDictCursor
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

        # create transaction
        query = """ SELECT * FROM recu_people """

        result = transaction_db(conn, query)

        return {"statusCode": 200, "body": json.dumps({"data": "Person created successfully", "result": result})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
    finally:
        conn.close()


def connection_db_postgres(host, user, password, database):
    conn_db = psycopg2.connect(host=host, user=user, password=password, database=database)
    return conn_db


def transaction_db(conn_db, query):
    cur = conn_db.cursor(cursor_factory=RealDictCursor)
    cur.execute(query)
    result = cur.fetchall()
    conn_db.commit()
    cur.close()

    return result
