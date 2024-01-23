try:
    import requests
except:
    import adafruit_requests as requests
import os

# SERVER = "192.168.1.228"
# PORT = "8000"
# URL = "http://" + SERVER + ":" + PORT + "/"

file = "img.jpg"
cwd = os.getcwd().replace("\\", "/") + "/"
location = cwd + file



def system_put(url, location):
    os.system("curl -X PUT --upload-file " + location + " " + url)

def system_get(url, location):
    file = location[location.rfind("/") + 1:]
    os.system("curl " + url + file + " --output recieved_" + file)

def requests_put(url, location):
    file = location[location.rfind("/") + 1:]
    headers = {"Content-type": "image/" + file[-3:], "path": file}
    # r = requests.put(url + file, files={file: (file, open(location, "rb"))}, headers=headers)
    r = requests.put(url + file, data=open(location, "rb"), headers=headers)
    r.raise_for_status()
def requests_get(url, location):
    file = location[location.rfind("/") + 1:]
    cwd = location[:location.rfind("/") + 1]
    r = requests.get(url + file)
    with open(cwd + "recieved_" + file, "wb") as f:
        f.write(r.content)

def action(url, action="TEST"):
    headers = {"action": action}
    r = requests.put(url, headers=headers)
    r.raise_for_status()