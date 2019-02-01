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
    username = {"username":username}

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
        return jsonify({"msg": "Bad username or password"}), 401

    user = {'username': username, 'id': user_id}

    access_token = JWT.encode(user, '69', algorithm='HS256')
    ret = {'access_token': str(access_token)}
    return jsonify(ret), 200


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

def getInfo(id):
    """

    :param id:
    :return:
    """
    cur, conn = connect_to_db()
    cur.execute("""SELECT * FROM users WHERE id=%s;""", id)
    user = cur.fetchall()[0]
    print(user)
    cur.close()
    conn.close()
    return flask.jsonify(user)


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
    return flask.jsonify(user)


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
    return flask.jsonify(user)


def get_secret(user, token_info):
    username = token_info['username']
    user_id = token_info['id']
    return '''
    You are user_id {username} and the secret is 'wbevuec'.
    Decoded token claims: {user_id}.
    '''.format(username=username, user_id=user_id)


