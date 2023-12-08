import base64
import os
import sqlite3
from sqlite3 import Error
from werkzeug.security import generate_password_hash

from flask import jsonify

from Database.db_get import calculate_average_pixel_color, find_closest_weather_data
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
def insertTimeTempHumid(temp, humid):
    connection = get_connection()
    try:
        cur = connection.cursor()
        # The time field will be automatically filled by the database
        cur.execute("INSERT INTO timetemphumid (temperature, humidity) VALUES (?, ?);", (temp, humid))
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

def insertImageWithTimestamp(filename, file_data, captured_at):
    connection = get_connection()
    try:
        cur = connection.cursor()

        # Insert image data into images table with captured timestamp
        cur.execute("INSERT INTO images (imageName, imageData, capturedAt) VALUES (?, ?, ?)", (filename, file_data, captured_at))
        image_id = cur.lastrowid

        # Calculate average color of the image
        avg_color = calculate_average_pixel_color(file_data)

        # Insert image metadata including avgColor
        cur.execute("INSERT INTO image_metadata (imageId, avgColor) VALUES (?, ?)", (image_id, avg_color))

        connection.commit()
        return image_id
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

def associateImageWithWeatherData(image_id, image_timestamp):
    # Find the closest weather data
    closest_weather_data = find_closest_weather_data(image_timestamp)
    if closest_weather_data:
        connection = get_connection()
        try:
            cur = connection.cursor()

            # Associate the image with the closest weather data
            timetemphumid_id = closest_weather_data[0]  # Assuming the first column is the ID
            cur.execute("UPDATE image_metadata SET timetemphumidId = ? WHERE imageId = ?", (timetemphumid_id, image_id))

            connection.commit()
        except Error as e:
            print(e)
        finally:
            if connection:
                connection.close()


def associateImageWithWeatherData(image_id, image_timestamp):
    # Find the closest weather data
    closest_weather_data = find_closest_weather_data(image_timestamp)
    if closest_weather_data:
        connection = get_connection()
        try:
            cur = connection.cursor()

            # Assume closest_weather_data[0] is the ID of the timetemphumid record
            timetemphumid_id = closest_weather_data[0]
            cur.execute("UPDATE image_metadata SET timetemphumidId = ? WHERE imageId = ?", (timetemphumid_id, image_id))

            connection.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            if connection:
                connection.close()