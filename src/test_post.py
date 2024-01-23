import requests
import os


URL = "http://192.168.1.42/upload"
response = requests.get(URL)
# open("img.jpg", "wb").write(response.content)

with open("C:/Users/ahpye/Desktop/dev/LED_Matrix_Spotify_API_[WIP]/img.bmp", 'rb') as f:
    files = {'upload_file': f.read()}
    
values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}

r = requests.post(URL, files=files, data=values)    