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

def get_message_groups(id):
    """

    :return:
    """
    info = {'id': id}
    cur, conn = connect_to_db()
    cur.execute("""SELECT * FROM message_groups WHERE user1=%(id)s OR user2=%(id)s OR user3=%(id)s""", info)
    chats = cur.fetchall()
    cur.close()
    conn.close()
    print(chats)
    return flask.jsonify(chats)


def get_chat(id):
    """

    :param id:
    :return:
    """
    cur, conn = connect_to_db()
    cur.execute("""SELECT * FROM messages WHERE messagegroup=%s ORDER BY timestamp;""", id)
    messages = cur.fetchall()
    print(messages)
    cur.close()
    conn.close()
    return flask.jsonify(messages)

def send_message(body):
    """

    :param body:
    :return:
    """
    cur, conn = connect_to_db()
    print(body)
    cur.execute("""INSERT INTO messages (content, messagegroup, fromid, fromname, timestamp) VALUES (%(content)s, %(messagegroup)s,
      %(from)s, %(fromname)s, %(timestamp)s)""", body)
    conn.commit()
    cur.close()
    conn.close()
