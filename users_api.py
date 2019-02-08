from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import flask
from flask import Flask, render_template,jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
import jwt as JWT
import json


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


def login(username, password):
    """

    :return:
    """
    cur, conn = connect_to_db()
    username = {"username": username}
    cur.execute("""SELECT id, password FROM users WHERE username=%(username)s""", username)
    user = cur.fetchall()
    if user == []:
        return 0
    print(user[0])
    cur.close()
    conn.close()
    if user[0]['password'] == password:
        return user[0]['id']
    else:
        return 0


def auth(body):
    username = body['username']
    password = body['password']
    user_id = login(username, password)
    if user_id == 0:
        return {"msg": "Bad username or password"}, 401

    user = {'username': username, 'id': user_id}
    access_token = JWT.encode(user, '69', algorithm='HS256')
    ret = {'token': str(access_token)}
    return ret


def create_user(body):
    """"""
    cur, conn = connect_to_db()
    cur.execute("""INSERT INTO users (username, email, firstname, lastname, password) VALUES (%(username)s,
      %(email)s,%(firstname)s,%(lastname)s, %(password)s);""", body)
    conn.commit()
    cur.close()
    conn.close()

    return "Success"

def getInfo(user, token_info):
    """

    :param id:
    :return:
    """
    username = token_info['username']
    id = token_info['id']
    cur, conn = connect_to_db()
    user_id = {'id': id}
    cur.execute("""SELECT * FROM users WHERE id=%(id)s;""", user_id)
    user = cur.fetchall()[0]
    cur.close()
    conn.close()
    return user


def getInfo_by_name(username):
    """

    :param username:
    :return:
    """
    cur, conn = connect_to_db()
    print(username)
    info = {'username': username}
    cur.execute("""SELECT * FROM users WHERE username=%(username)s;""", info)
    user = cur.fetchall()[0]
    print(user)
    cur.close()
    conn.close()
    return user


def get_posts_by_id(user, token_info):
    """

    :param username:
    :return:
    """
    username = token_info['username']
    id = token_info['id']
    cur, conn = connect_to_db()
    info = {'id': id}
    cur.execute("""SELECT * FROM posts WHERE userid=%(id)s;""", info)
    user = cur.fetchall()
    print(user)
    cur.close()
    conn.close()
    return user


def get_secret(user, token_info):
    username = token_info['username']
    user_id = token_info['id']
    return '''
    You are user_id {username} and the secret is 'wbevuec'.
    Decoded token claims: {user_id}.
    '''.format(username=username, user_id=user_id)


def decode_token(token):
    print(token.split("'")[1])
    ret = JWT.decode(token.split("'")[1], '69', algorithms=['HS256'])
    print(ret)
    return ret


def lambda_handler(event, context):
    op = event["queryStringParameters"]['operation']
    query = event["queryStringParameters"]['info']
    result = []
    if op == 'auth':
        result = auth(json.loads(event['body']))

    elif op == 'create_user':
        create_user(json.loads(event['body']))
        return {
            'statusCode': 200
        }

    elif op == 'user_info':
        token_info = decode_token(event['headers']['Authorization'])
        result = getInfo('', token_info)

    elif op == 'user_info_name':
        result = getInfo_by_name(query)

    else:
        return {
            'statusCode': 500,
            'body': json.dumps(op)
        }

    return {
        'statusCode': 200,
        'body': json.dumps(result),
        'headers': {"Access-Control-Allow-Origin": "*"}
    }

