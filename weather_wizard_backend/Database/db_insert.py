import base64
import os
import sqlite3
from sqlite3 import Error

from flask import jsonify

from weather_wizard_backend.Database.db_setup import get_connection


def insertImage(filename, file):
    connection = get_connection()
    try:
        cur = connection.cursor()

        # Insert into the database
        cur.execute("INSERT INTO images (imageName, imageData) VALUES (?, ?)",
                    (filename, file))
        connection.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

def insertTimeTempHumid(time, temp, humid):
    connection = get_connection()
    try:
        cur = connection.cursor()
        # Select all data from timetemphumid table
        data = cur.execute("INSERT INTO timetemphumid VALUES (?, ?);", (time, temp, humid))
        connection.commit()
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()