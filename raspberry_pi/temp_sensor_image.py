
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
    
# timestamp = '2024-10-31 05:45:35'
# temperature = 50.0
# humidity = 10.0
# data_server_url = 'http://192.168.0.199:5000/raspi_upload_data'
# data_response = upload_data(timestamp, temperature, humidity, data_server_url)

def main_program():
    URL = 'host:port/endpoint'
    while True:
        # Replace 'your_folder_path' with the path to your image folder
        folder_path = '/home/raspi/project/images'

        # Replace 'your_server_url' with the URL where you want to upload the images
        server_url = 'http://192.168.0.199:5000/raspi_upload_image'

        image_response = upload_images(folder_path, server_url)
        #data_response = upload_data(timestamp, temperature, humidity)
        time.sleep(900)  # 3600 seconds in an hour
with daemon.DaemonContext():
    main_program()
