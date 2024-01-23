from dotenv import load_dotenv
import os
import requests
import time
from urllib.parse import urlencode
import base64
import webbrowser
import cv2
import numpy as np


load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
auth_code = os.getenv("AUTHORIZATION_CODE")

auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": "http://localhost:7777/callback",
    "scope": "user-read-currently-playing"
}

webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))

auth_code = input("What is your authorization url?")
auth_code = auth_code[-(len(auth_code) - 36):]

encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

token_headers = {
    "Authorization": "Basic " + encoded_credentials,
    "Content-Type": "application/x-www-form-urlencoded"
}

token_data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": "http://localhost:7777/callback"
}

r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)

if r.status_code != 200:
    raise Exception("Status code: " + str(r.status_code))


access_token = r.json()["access_token"]

print(r.json)
print("Access Token: " + access_token)

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'


def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    json_resp = response.json()

    try:
        track_id = json_resp['item']['id']
        track_name = json_resp['item']['name']
        artists = [artist for artist in json_resp['item']['artists']]
        cover_art = json_resp['item']['album']['images'][0]['url']

        link = json_resp['item']['external_urls']['spotify']

        artist_names = ', '.join([artist['name'] for artist in artists])

        current_track_info = {
            "id": track_id,
            "track_name": track_name,
            "artists": artist_names,
            "cover_art": cover_art,
            "link": link
        }
    except:
        current_track_info = {
            "id": -1,
        }

    return current_track_info

def download_image(url):
    data = requests.get(url).content 
    with open('LED_Matrix_Spotify_API_[WIP]/img.jpg','wb') as f:
        f.write(data) 
    img = cv2.imread('LED_Matrix_Spotify_API_[WIP]/img.jpg')
    res = cv2.resize(img, dsize=(32, 32), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite('LED_Matrix_Spotify_API_[WIP]/img.bmp', res) 

def main():
    current_track_id = None
    while True:
        current_track_info = get_current_track(access_token)

        if current_track_info['id'] != current_track_id:
            if current_track_info['id'] == -1:
                print("AD!")
            else:
                print(
                    current_track_info
                )
                current_track_id = current_track_info['id']
                download_image(current_track_info['cover_art'])

        time.sleep(1)


if __name__ == '__main__':
    main()