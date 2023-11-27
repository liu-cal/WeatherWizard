import atexit
import os

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from Database.db_get import fetchImages, fetchTimeTempHumid, fetchUsers, fetchUserByUsernameAndPassword
from Database.db_insert import insertUser, insertImage
from Database.db_setup import create_connection, insertDefaultImages, deleteAllImages, deleteAllTimeTempHumidData, \
    insertFakeTimeTempHumidData, insertDummyUser, deleteAllUsers

from werkzeug.utils import secure_filename

import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'weather-wizard'  # Change this to a secret key of your choice

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    # Return a User object if the user exists, otherwise return None
    users = fetchUsers().json
    for user in users:
        if user['id'] == int(user_id):
            u = User()
            u.id = user['id']
            return u
    return None

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Insert into the database (you need to implement this function)
        insertUser(username, password)

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_response = fetchUserByUsernameAndPassword(username, password)

        if 'id' in user_response.json:  # Check if user found
            # Log the user in
            u = User()
            u.id = user_response.json['id']
            login_user(u)
            return redirect(url_for('index'))
        else:
            error_message = user_response.json['message']
            flash(error_message, 'error')

    return render_template('login.html', error_message=error_message)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/line_graph')
@login_required
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
@login_required
def result():
    images = fetchImages().get_json()  # Fetch images from the database
    return render_template('result.html', image_files=images)


@app.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            filename = secure_filename(image.filename)
            file_path = os.path.join('uploads', filename)
            image.save(file_path)

            # Open the file in binary mode and read
            with open(file_path, 'rb') as file:
                file_data = file.read()

            # Insert image into the database
            insertImage(filename, file_data)

            # Optionally, remove the image file after saving to database
            os.remove(file_path)

            flash('Image uploaded successfully!', 'success')
        else:
            flash('No selected file', 'error')
    return redirect(url_for('result'))

if __name__ == '__main__':
    create_connection()
    insertDefaultImages()
    fetchTimeTempHumid()
    insertFakeTimeTempHumidData()
    insertDummyUser()

    # Start the Flask application
    app.run(debug=True)

# Register the deleteAllImages function to be called when the application ends
atexit.register(deleteAllImages)
atexit.register(deleteAllTimeTempHumidData)
atexit.register(deleteAllUsers)
