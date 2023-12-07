import base64
import os
import sqlite3
from sqlite3 import Error
from werkzeug.security import generate_password_hash

from flask import jsonify

from Database.db_get import calculate_average_pixel_color
from Database.db_setup import get_connection


def insertImage(filename, file_data):
    connection = get_connection()
    try:
        cur = connection.cursor()

        # Insert image data into images table
        cur.execute("INSERT INTO images (imageName, imageData) VALUES (?, ?)", (filename, file_data))
        image_id = cur.lastrowid

        # Calculate average color of the image
        avg_color = calculate_average_pixel_color(file_data)

        # Insert image metadata including avgColor
        cur.execute("INSERT INTO image_metadata (imageId, avgColor) VALUES (?, ?)", (image_id, avg_color))

        connection.commit()
        return image_id  # Optionally return the image ID
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()
def insertTimeTempHumid(time, temp, humid):
    connection = get_connection()
    try:
        cur = connection.cursor()
        # Select all data from timetemphumid table
        data = cur.execute("INSERT INTO timetemphumid (time, temperature, humidity) VALUES (?, ?, ?);", (time, temp, humid))
        connection.commit()
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

def insertUser(username, password):
    connection = get_connection()
    try:
        cur = connection.cursor()

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password)

        # Insert into the database
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, hashed_password))

        connection.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if connection:
            connection.close()
