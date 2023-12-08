import sqlite3
from sqlite3 import Error
import os
from werkzeug.security import generate_password_hash


def get_connection():
    return sqlite3.connect('weather.db')


def create_connection():
    connection = get_connection()

    try:
        with open('schema.sql') as f:
            connection.executescript(f.read())
        connection.commit()
        connection.close()
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()


def insertDefaultImages():
    connection = get_connection()
    try:
        cur = connection.cursor()

        # List of default image filenames
        image_filenames = [
            "images_image0.png",
            "images_image1698859268.png",
            "images_image1698859291.png",
            "images_image1698859321.png",
            "images_image1698859351.png"
        ]

        for filename in image_filenames: #make this a ``for i in x:`` loop to add image_colors
            # Construct the file path and read the image in binary mode
            file_path = os.path.join('uploads', filename)
            with open(file_path, 'rb') as file:  # Note the 'rb' mode here for binary read
                image_data = file.read()

            # Insert into the database
            cur.execute("INSERT INTO images (imageName, imageData) VALUES (?, ?)",
                        (filename, image_data))

        connection.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

def insertFakeTimeTempHumidData():
    connection = get_connection()
    try:
        cur = connection.cursor()
        # List of fake time, temperature, and humidity data
        time_temp_humid_data = [
            ('2023-10-31 05:45:35', 22.89, 38.4),
            ('2023-11-01 18:10:10', 22.3, 30.32),
            ('2023-11-02 18:10:15', 23.1, 35.5),
            ('2023-11-03 18:10:20', 21.9, 33.8),
            ('2023-11-04 18:10:25', 24.2, 29.4),
            ('2023-11-05 18:10:30', 22.8, 37.6),
            ('2023-11-06 18:10:35', 23.5, 36.1),
            ('2023-11-07 18:10:40', 21.7, 38.9),
            ('2023-11-08 18:10:45', 22.9, 34.7),
            ('2023-11-09 18:10:50', 23.3, 32.0),
            ('2023-11-10 18:10:55', 24.0, 30.5),
            # Add more data as needed
        ]
        for record in time_temp_humid_data:
            # Insert data into the database
            cur.execute("INSERT INTO timetemphumid (time, temperature, humidity) VALUES (?, ?, ?)",
                        record)
        connection.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if connection:
            connection.close()



def deleteAllTimeTempHumidData():
    connection = get_connection()
    try:
        cur = connection.cursor()
        # Delete all records from the timetemphumid table
        cur.execute("DELETE FROM timetemphumid;")
        connection.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

def deleteAllImages():
    connection = get_connection()
    try:
        cur = connection.cursor()
        # Delete all records from the images table
        cur.execute("DELETE FROM images;")
        connection.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

def insertDummyUser():
    connection = get_connection()
    try:
        cur = connection.cursor()

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash("password")

        # Insert into the database
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                    ("user", hashed_password))

        connection.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

def deleteAllUsers():
    connection = get_connection()
    try:
        cur = connection.cursor()
        # Delete all records from the users table
        cur.execute("DELETE FROM users;")
        connection.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if connection:
            connection.close()


def deleteAllImageMetadata():
    connection = get_connection()
    try:
        cur = connection.cursor()
        # Delete all records from the image_metadata table
        cur.execute("DELETE FROM image_metadata;")
        connection.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if connection:
            connection.close()
