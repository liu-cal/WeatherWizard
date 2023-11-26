import atexit

from Database.db_get import fetchImages

from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px

from Database.db_setup import create_connection, insertDefaultImages, deleteAllImages


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/line_graph')
def line_graph():
    # Read the CSV file
    df = pd.read_csv('static/temperature_humidity_data.csv', names=['Time', 'Temperature', 'Humidity'])

    # Create a line graph
    fig = px.line(df, x='Time', y='Temperature', title='Temperature Over Time')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        'line_graph.html',
        labels=df['Time'].tolist(),
        data_temperature=df['Temperature'].tolist(),
        data_humidity=df['Humidity'].tolist(),
        header="Temperature and Humidity Over Time",
        description="Graph shows temperature and humidity changes over time."
    )

@app.route('/result', methods=['GET'])
def result():
    images = fetchImages().get_json()  # Fetch images from the database
    return render_template('result.html', image_files=images)

def main():
    create_connection()
    insertDefaultImages()

    # Start the Flask application
    app.run(debug=True)

# Register the deleteAllImages function to be called when the application ends
atexit.register(deleteAllImages)

if __name__ == '__main__':
    main()

