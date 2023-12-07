import base64


from PIL import Image
from sqlite3 import Error
import numpy as np
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

def fetch_avg_colors_and_compare(avg_color):
    connection = get_connection()
    try:
        cur = connection.cursor()
        # Join the 'image_metadata' and 'images' tables on the 'imageId' field
        cur.execute("""
            SELECT image_metadata.id, images.imageData 
            FROM image_metadata 
            INNER JOIN images ON image_metadata.imageId = images.id;
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
        cur.execute("SELECT timetemphumidId FROM image_metadata WHERE id = ?;", (image_id,))
        timetemphumid_id = cur.fetchone()[0]
        cur.execute("SELECT Temperature, Humidity FROM timetemphumid WHERE id = ?;", (timetemphumid_id,))
        temperature, humidity = cur.fetchone()
        return temperature, humidity
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()


def calculate_average_pixel_color(image_path):
    try:
        # Open the image file
        image = Image.open(image_path)

        # Convert the image to RGB mode if it's not already in RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Get the width and height of the image
        width, height = image.size

        # Initialize variables to store the sum of RGB values
        sum_red = 0
        sum_green = 0
        sum_blue = 0

        # Iterate over each pixel in the image
        for y in range(height):
            for x in range(width):
                # Get the RGB values of the pixel
                red, green, blue = image.getpixel((x, y))

                # Add the RGB values to the sum
                sum_red += red
                sum_green += green
                sum_blue += blue

        # Calculate the average RGB values
        num_pixels = width * height
        average_red = sum_red // num_pixels
        average_green = sum_green // num_pixels
        average_blue = sum_blue // num_pixels

        # Return the average pixel color as a tuple
        return (average_red, average_green, average_blue)

    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found at path: {image_path}")

    except Exception as e:
        raise ValueError(f"Invalid image file: {e}")