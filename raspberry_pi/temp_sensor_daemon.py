import Adafruit_DHT
import time
import csv
import os
import daemon
from datetime import datetime
from PIL import Image
import io

import os
import requests

def upload_images(folder_path, server_url):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    last_modified_file = max(files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
    new_path = folder_path + "/" + last_modified_file
    
    with open(new_path, 'rb') as file:
        files = {'image': (new_path, file)}
        cred = {'username': 'admin', 'password': 'secret'}
        response = requests.post(server_url, files=files, data=cred)


    return response

# def get_last_file(folder_path):
    # files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # if not files:
        # return None  # No files in the folder

    # # Sort files by modification time and get the last one
    # last_file = max(files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))

    # return last_file

# Print the server's response
print(response.text)


def main_program():
    URL = 'host:port/endpoint'

    # Set your DHT sensor type and pin
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 6  # Replace with the actual GPIO pin where your sensor is connected

    # File to save the data
    CSV_FILE = "/home/raspi/project/log/temperature_humidity_data.csv"
    while True:
        # Get the current date and time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Attempt to read data from the sensor
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

        # Check if data reading is successful
        if humidity is not None and temperature is not None:
            # Print the data (optional)
            print(f"{timestamp} - Temp={temperature:.1f}°C  Humidity={humidity:.1f}%")

            # Write the data to the CSV file
            with open(CSV_FILE, "a") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([timestamp, temperature, humidity])

        else:
            print("Failed to retrieve data from the sensor.")

        # Wait for one hour
        # Replace 'your_folder_path' with the path to your image folder
        folder_path = '/home/raspi/project/images'

        # Replace 'your_server_url' with the URL where you want to upload the images
        server_url = 'http://192.168.0.199:5000/raspi_upload_image'

        response = upload_images(folder_path, server_url)
        time.sleep(900)  # 3600 seconds in an hour
with daemon.DaemonContext():
    main_program()
