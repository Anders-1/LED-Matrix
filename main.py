import displayio
from adafruit_matrixportal.matrix import Matrix
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
import board
import gc
import time
import adafruit_requests
from adafruit_matrixportal.network import Network
import json
from adafruit_datetime import datetime


secrets = {
    "openweather_token": "dff714e2d2b94c3cde7f928b06d13dfd"
}

LOCATION = "Hyattsville, US"
DATA_SOURCE = (
    "http://api.openweathermap.org/data/2.5/weather?q=" + LOCATION + "&units=" + "imperial" + "&appid=" + secrets["openweather_token"]
)

TEXT_COLOR = 0xffffff

font = bitmap_font.load_font("./fonts/4x6.bdf")
glyphs = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: "
font.load_glyphs(glyphs)

matrix = Matrix()
network = Network(status_neopixel=board.NEOPIXEL, debug=True)
display = matrix.display
text_group = displayio.Group()

def get_weather():
    # r = adafruit_requests.get(DATA_SOURCE)
    r = network.fetch_data(DATA_SOURCE)
    print("REQUEST: " + r)
    data = json.loads(r)
    # data = r.json()
    data = {
        "weather": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
        "temp_min": round(data["main"]["temp_min"]),
        "temp_max": round(data["main"]["temp_max"]),
        "wind": round(data["wind"]["speed"]),
    }
    return data

weather = get_weather()

def text(text_group = text_group, font=font, x=20, y=7, color=TEXT_COLOR, text=None):
    new_text = Label(font, x=x, y=y, color=color, text=text)
    text_group.append(new_text)
    return new_text

global_time = network.get_local_time("America/New_York")
time_text = text(x=32, y=7, text=global_time[11:16])
song_text = text(x=32, y=14, text="Loading...")
summary_text = text(x=32, y=21, text=weather["weather"])
temp_text = text(x=32, y=28, text="-".join([str(weather["temp_min"]), str(weather["temp_max"])]))

first_run = True
reverse = False
left_padding = 3
right_padding = 3

while True:
    global_time = str(datetime.now())
    time_text.text = global_time[11:16].lstrip("0")


    song_text.text = "vfx posy is so cool!"

    text_length = len(song_text.text) * 4

    if reverse: 
        song_text.x = song_text.x + 1
    elif not reverse:
        song_text.x = song_text.x - 1

    if song_text.x + text_length <= (64 - left_padding):
        reverse = True
    elif song_text.x >= (32 + right_padding):
        reverse = False

    if float(global_time[14:19].replace(":", ".")) % 15 == 0:
        weather = get_weather()
        summary_text.text = weather["weather"]
        temp_text.text = "-".join([str(weather["temp_min"]), str(weather["temp_max"])])
        del weather

    display.show(text_group)

    bitmap = displayio.OnDiskBitmap("img.bmp")
    tilegrid = displayio.TileGrid(
        bitmap,
        # pixel_shader=getattr(bitmap, 'pixel_shader', displayio.ColorConverter()),
        pixel_shader=bitmap.pixel_shader,
        tile_width=bitmap.width,
        tile_height=bitmap.height,
    )
    if first_run == False:
        text_group[-1] = tilegrid
    else:
        text_group.append(tilegrid)
    display.show(text_group)
    del tilegrid
    del global_time
    del text_length
    gc.collect()
    # print(gc.mem_free())
    time.sleep(0.5)
    if first_run == True:
        first_run = False
