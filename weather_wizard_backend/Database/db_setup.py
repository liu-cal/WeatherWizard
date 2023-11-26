import sqlite3
from sqlite3 import Error
import os


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

        for filename in image_filenames:
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
