
import sqlite3
from sqlite3 import Error
from werkzeug.security import generate_password_hash
import math
import datetime

from Database.db_get import find_closest_weather_data
from Database.db_setup import get_connection, calculate_average_pixel_color


def insertImage(filename, file_data):
   connection = get_connection()
   try:
       cur = connection.cursor()

       # Insert image data into images table
       cur.execute("INSERT INTO images (imageName, imageData) VALUES (?, ?)", (filename, file_data))
       image_id = cur.lastrowid

       # Calculate average color of the image
       avg_color = calculate_average_pixel_color(file_data)

       # Fetch average color and timetemphumidId of all images in image_metadata table
       cur.execute("SELECT avgColor, timetemphumidId FROM image_metadata")
       image_metadata = cur.fetchall()

       # Find the image with the closest average color
       closest_color_diff = float('inf')
       closest_timetemphumidId = None
       for metadata in image_metadata:
           color_diff = calculate_color_difference(avg_color, metadata[0])
           if color_diff < closest_color_diff:
               closest_color_diff = color_diff
               closest_timetemphumidId = metadata[1]

       # Fetch the closest timetemphumid record
       cur.execute("SELECT * FROM timetemphumid WHERE id = ?", (closest_timetemphumidId,))
       closest_timetemphumid = cur.fetchone()

       # Create a new timetemphumid record with the same temperature and humidity, and the current time
       current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       cur.execute("INSERT INTO timetemphumid (time, temperature, humidity) VALUES (?, ?, ?)",
                 (current_time, closest_timetemphumid[2], closest_timetemphumid[3]))
       new_timetemphumidId = cur.lastrowid

       # Insert image metadata including avgColor and the new timetemphumidId
       cur.execute("INSERT INTO image_metadata (imageId, avgColor, timetemphumidId) VALUES (?, ?, ?)",
                 (image_id, avg_color, new_timetemphumidId))

       connection.commit()
       return image_id # Optionally return the image ID
   except Error as e:
       print(e)
   finally:
       if connection:
           connection.close()

def calculate_color_difference(color1, color2):
   color1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
   color2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
   return math.sqrt((color2[0] - color1[0])**2 + (color2[1] - color1[1])**2 + (color2[2] - color1[2])**2)

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