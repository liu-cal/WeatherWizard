import base64
import csv
import io
from datetime import datetime
from Database.db_insert import insertImage, insertTimeTempHumid
from PIL import Image
from flask import Flask, request, render_template, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename, send_from_directory

import os
import atexit

from Database.db_get import fetchImages

from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px

from Database.db_setup import create_connection, insertDefaultImages, deleteAllImages
from Database.db_setup import (create_connection, insertDefaultImages,
                               deleteAllImages, insertFakeTimeTempHumidData, deleteAllTimeTempHumidData)
from Database.db_get import fetchTimeTempHumid


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # This is where I defined the folder

# To catch if the folder does not exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/line_graph')
def line_graph():

    # Fetch data from the TIMETEMPHUMID table
    time_temp_humid_data = fetchTimeTempHumid()


    # Check if data is not empty and is in the expected format
    if time_temp_humid_data and isinstance(time_temp_humid_data, list):
        # Create a DataFrame from the fetched data
        df = pd.DataFrame(time_temp_humid_data)

        # Prepare data for Chart.js
        labels = df['Time'].tolist()
        data_temperature = df['Temperature'].tolist()
        data_humidity = df['Humidity'].tolist()
    else:
        # If no data, provide empty values
        labels, data_temperature, data_humidity = [], [], []

    return render_template(
        'line_graph.html',
        labels=labels,
        data_temperature=data_temperature,
        data_humidity=data_humidity
    )



@app.route('/result', methods=['GET'])
def result():
    images = fetchImages().get_json()  # Fetch images from the database
    return render_template('result.html', image_files=images)

def main():
    create_connection()
    insertDefaultImages()
    fetchTimeTempHumid()
    insertFakeTimeTempHumidData()
    app.run(host='0.0.0.0', port=5000, debug=True)

# Register the deleteAllImages function to be called when the application ends
atexit.register(deleteAllImages)
atexit.register(deleteAllTimeTempHumidData)

def read_images_as_byte_arrays(folder_path):
    # Initialize an empty list to store byte arrays
    image_byte_arrays = []

    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the file is an image (you may want to add more file format checks)
        if file_path.lower().endswith(('.png')):
            # Open the image using Pillow (PIL)
            with Image.open(file_path) as img:
                # Convert the image to bytes
                img_byte_array = io.BytesIO()
                img.save(img_byte_array, format='PNG')  # You can change the format as needed
                img_byte_array = img_byte_array.getvalue()

                # Append the byte array to the list
                image_byte_arrays.append(img_byte_array)

    return image_byte_arrays


@app.route('/sendImages', methods=['GET', 'POST'])
def sendImages():
    if request.method == 'POST':
        files = request.files.getlist('images')

        for file in files:
            # Save or process each file as needed
            # For example, you can save the file to a specific folder
            file.save('uploads/' + file.filename)
        img_array = read_images_as_byte_arrays("uploads/")
        for file in img_array:
            insertImage("filename", file)
        return 'Images uploaded successfully.'

    else:
        return render_template('index.html')


@app.route('/sendData', methods=['GET', 'POST'])
def sendTimeTempHumid():
    if request.method == 'POST':
        data = request.get_json()

        # Accessing float values from the JSON data
        time = data.get(0)
        temp = data.get(1)
        humid = data.get(2)

        insertTimeTempHumid(time, temp, humid)
        return 'Data uploaded successfully.'

    else:
        return render_template('index.html')


# @appFlask.route('/test', methods=['GET', 'POST'])
# def test():
#     if request.method == 'POST':
#         files = request.files.getlist('images')
#
#         for file in files:
#             # Save or process each file as needed
#             # For example, you can save the file to a specific folder
#             file.save('uploads/' + file.filename)
#
#         return 'Images uploaded successfully.'
#     if request.method == 'GET':
#         return "haha"


def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif', 'bmp'}




@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(appFlask.config['UPLOAD_FOLDER'], filename)


# @app.route('/')
# def index():
#     if request.method == 'POST':
#         return "hihi"
#     if request.method == 'GET':
#         return render_template('index.html')
#
#
#
# @app.route('/line_graph')
# def line_graph():
#     # Read the CSV file
#     df = pd.read_csv('static/temperature_humidity_data.csv', names=['Time', 'Temperature', 'Humidity'])
#
#     # Create a line graph
#     fig = px.line(df, x='Time', y='Temperature', title='Temperature Over Time')
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#
#     return render_template(
#         'line_graph.html',
#         labels=df['Time'].tolist(),
#         data_temperature=df['Temperature'].tolist(),
#         data_humidity=df['Humidity'].tolist(),
#         header="Temperature and Humidity Over Time",
#         description="Graph shows temperature and humidity changes over time."
#     )

if __name__ == '__main__':
    main()
