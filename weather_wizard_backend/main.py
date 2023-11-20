# import base64
# import csv
#
# from flask import Flask, request, render_template, jsonify
# from werkzeug.utils import secure_filename, send_from_directory
#
# import os
#
# appFlask = Flask(__name__)
# appFlask.config['UPLOAD_FOLDER'] = 'uploads/'  # This is where I defined the folder
#
# # To catch if the folder does not exist
# os.makedirs(appFlask.config['UPLOAD_FOLDER'], exist_ok=True)
#
#
# # db = SQLAlchemy(appFlask)
#
# @appFlask.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         # Retrieve files from the 'folder_input' field
#         files = request.files.getlist("folder_input")
#         image_files = []
#         for file in files:
#             if file and allowed_file(file.filename):
#                 # Save the file and add it to the image_files list
#                 filename = secure_filename(file.filename)
#                 file_path = os.path.join(appFlask.config['UPLOAD_FOLDER'], filename)
#                 file.save(file_path)
#                 image_files.append(file_path)
#
#         if image_files:
#             # No need to send the full paths to the template
#             return render_template('result.html', image_files=image_files)
#         else:
#             return render_template('result.html', image_files=None)
#
#     return render_template('index.html')
#
# def render_picture(data):
#
#     render_pic = base64.b64encode(data).decode('ascii')
#     return render_pic
#
# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
#
#
# @appFlask.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(appFlask.config['UPLOAD_FOLDER'], filename)
#
#
# if __name__ == '__main__':
#     appFlask.run(debug=True, port=5000)
from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px

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


if __name__ == '__main__':
    app.run(debug=True)
