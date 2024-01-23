# import requests

# API_KEY = 'dff714e2d2b94c3cde7f928b06d13dfd'
# API_ENDPOINT = 'http://api.weatherapi.com/v1/current.json'
# location = '38.972495, -76.947978'

# payload = {'key': API_KEY, 
#         'q': location,}
# r = requests.get(API_ENDPOINT, json=payload)
# print(r)

import requests
secrets = {
    "openweather_token": "dff714e2d2b94c3cde7f928b06d13dfd"
}

LOCATION = "Hyattsville, US"
DATA_SOURCE = (
    "http://api.openweathermap.org/data/2.5/weather?q=" + LOCATION + "&units=" + "imperial" + "&appid=" + secrets["openweather_token"]
)
r = requests.get(DATA_SOURCE)
data = r.json()
data = {
    "weather": data["weather"][0]["main"],
    "description": data["weather"][0]["description"],
    "temp_min": round(data["main"]["temp_min"]),
    "temp_max": round(data["main"]["temp_max"]),
    "wind": round(data["wind"]["speed"]),
}
print(data)
