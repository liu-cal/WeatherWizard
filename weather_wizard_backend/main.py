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


    # Start the Flask application
    app.run(debug=True)

# Register the deleteAllImages function to be called when the application ends
atexit.register(deleteAllImages)
atexit.register(deleteAllTimeTempHumidData)

if __name__ == '__main__':
    main()