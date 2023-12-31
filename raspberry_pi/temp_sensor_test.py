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
    
def upload_data(temp, humid, server_url):
    cred = {'username': 'admin', 'password': 'secret', 'temperature': temp, 'humidity': humid}
    response = requests.post(server_url, data=cred)


    return response

# def get_last_file(folder_path):
    # files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # if not files:
        # return None  # No files in the folder

    # # Sort files by modification time and get the last one
    # last_file = max(files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))

    # # return last_file
# timestamp = '2024-10-31 05:45:35'
# temperature = 50.0
# humidity = 10.0
# data_server_url = 'http://192.168.0.199:5000/raspi_upload_data'
# data_response = upload_data(timestamp, temperature, humidity, data_server_url)

def main_program():
    URL = 'host:port/endpoint'

    # Set your DHT sensor type and pin
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 4  # Replace with the actual GPIO pin where your sensor is connected

    # File to save the data
    CSV_FILE = "/home/raspi/project/log/temperature_humidity_data.csv"
    while True:
        # Get the current date and time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # Attempt to read data from the sensor
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        except Exception as e:
            print(f"Error getting sensor data: {e}")
        
        # Print the data (optional)
        print(f"{timestamp} - Temp={temperature:.1f}°C  Humidity={humidity:.1f}%")

        # Check if data reading is successful
        if humidity is not None and temperature is not None:
            try:
                with open(CSV_FILE, "a") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([timestamp, temperature, humidity])
            except Exception as e:
                print(f"Error writing to CSV: {e}")

        else:
            print("Failed to retrieve data from the sensor.")

        # Wait for one hour
        # Replace 'your_folder_path' with the path to your image folder
        folder_path = '/home/raspi/project/images'

        # Replace 'your_server_url' with the URL where you want to upload the images
        data_server_url = 'http://192.168.0.199:5000/raspi_insert_time_temp_humid'

        #image_response = upload_images(folder_path, server_url)
        data_response = upload_data(temperature, humidity, data_server_url)
        time.sleep(300)  # 3600 seconds in an hour
with daemon.DaemonContext():
    main_program()
