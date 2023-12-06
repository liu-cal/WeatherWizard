import base64
import os
import sqlite3
from sqlite3 import Error
import numpy as np

from flask import jsonify

from Database.db_setup import get_connection
from werkzeug.security import check_password_hash

from main import calculate_average_pixel_color


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

def fetch_avg_colors_and_compare(avg_color):
    connection = get_connection()
    try:
        cur = connection.cursor()
        # Join the 'color' and 'images' tables on the 'imageId' field
        cur.execute("""
            SELECT color.id, images.imageData 
            FROM color 
            INNER JOIN images ON color.imageId = images.id;
        """)
        images = cur.fetchall()
        connection.commit()

        color_diffs = {}

        for img in images:
            img_id = img[0]
            img_data = img[1]
            # Calculate the average pixel color of the image data
            avg_pixel_color = calculate_average_pixel_color(img_data)
            color_diff = np.abs(np.subtract(avg_color, avg_pixel_color))
            color_diffs[img_id] = np.sum(color_diff)

        closest_img_id = min(color_diffs, key=color_diffs.get)
        return closest_img_id

    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

def fetch_temperature_and_humidity(image_id):
    connection = get_connection()
    try:
        cur = connection.cursor()
        cur.execute("SELECT timetemphumidId FROM color WHERE id = ?;", (image_id,))
        timetemphumid_id = cur.fetchone()[0]
        cur.execute("SELECT Temperature, Humidity FROM timetemphumid WHERE id = ?;", (timetemphumid_id,))
        temperature, humidity = cur.fetchone()
        return temperature, humidity
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

