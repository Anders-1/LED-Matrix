import os
import file_client

SERVER = "192.168.1.228"
PORT = "8000"
URL = "http://" + SERVER + ":" + PORT + "/"

file = "goofy.jpg"
cwd = os.getcwd().replace("\\", "/") + "/"
location = cwd + file

file_client.requests_get(URL, location)