import base64
import os
import sqlite3
from sqlite3 import Error

from flask import jsonify

from weather_wizard_backend.Database.db_setup import get_connection


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