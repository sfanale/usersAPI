from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import flask


# 3rd party modules
from flask import make_response, abort


def connect_to_db():
    """
    This function uses the psycopg2 library to connect to an RDS instance where the tables for this project are
    being stored. I currently have the information here and I should remove it.
    :return: cursor and connection objects for interacting with the table
    """
    try:
        conn = psycopg2.connect(host="options-prices.cetjnpk7rvcs.us-east-1.rds.amazonaws.com", database="options_prices",
                            user="Stephen", password="password69")
        cur = conn.cursor(cursor_factory=RealDictCursor)
        return cur, conn
    except ConnectionRefusedError:
        return "Connection Refused"

def login(body):
    """

    :return:
    """
    cur, conn = connect_to_db()
    user = {}

    cur.execute("""SELECT id, password FROM users WHERE username=%(username)s""", body)
    user = cur.fetchall()[0]
    print(user)
    if user['password'] == body['password']:
        # return a key or something?
        return flask.jsonify({'id': user['id']})
    else:
        return 'bad password'


def create_user(body):
    """"""
    cur, conn = connect_to_db()
    print(body)

    cur.execute("""INSERT INTO users (username, email, firstname, lastname, password, birthdate) VALUES (%(username)s,
      %(email)s,%(firstname)s,%(lastname)s, %(password)s, %(birthdate)s);""", body)
    conn.commit()
    cur.close()
    conn.close()

    return "Success"
