import base64
import os
import sqlite3
from sqlite3 import Error

from flask import jsonify

from Database.db_setup import get_connection
from werkzeug.security import check_password_hash

def fetchImages():
    connection = get_connection()
    try:
        cur = connection.cursor()
        images = cur.execute("SELECT * FROM images;").fetchall()
        connection.commit()

        # Correctly handle the image data
        image_list = [{
            'id': img[0],
            'imageName': img[1],
            'imageData': base64.b64encode(img[2]).decode('utf-8')  # Encode as base64
        } for img in images]

        return jsonify(image_list)
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()


def fetchTimeTempHumid():
    connection = get_connection()
    try:
        cur = connection.cursor()
        # Select all data from timetemphumid table
        data = cur.execute("SELECT * FROM timetemphumid;").fetchall()
        connection.commit()
        # Convert the data to a list of dictionaries for processing
        result = [{'Time': row[1], 'Temperature': row[2], 'Humidity': row[3]} for row in data]
        return result
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()


def fetchUsers():
    connection = get_connection()
    try:
        cur = connection.cursor()
        # Select all data from the users table
        users = cur.execute("SELECT * FROM users;").fetchall()
        connection.commit()

        # Convert the data to a list of dictionaries for processing
        user_list = [{
            'id': user[0],
            'username': user[1],
            'password': user[2]
        } for user in users]

        return jsonify(user_list)
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()


def fetchUserByUsernameAndPassword(username, password):
    connection = get_connection()
    try:
        cur = connection.cursor()

        # Select user based on username
        cur.execute("SELECT * FROM users WHERE username = ?;", (username,))
        user = cur.fetchone()

        if user and check_password_hash(user[2], password):
            # Prepare the user data for JSON response
            result = {
                'id': user[0],
                'username': user[1],
                'password': user[2],
            }

            return jsonify(result)
        else:
            return jsonify({'message': 'Invalid username or password'})

    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

