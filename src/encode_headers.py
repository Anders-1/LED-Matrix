auth_headers = {
    "client_id": "client_id",
    "response_type": "code",
    "redirect_uri": "http://localhost:7777/callback",
    "scope": "user-read-currently-playing"
}

def encode_headers(headers):
    result = ""
    for key, value in headers.items():
        if list(headers.keys()).index(key) != 0:
            result += "&"
        result += key + "=" + value
    return result


# https://accounts.spotify.com/authorize?client_id=801e463eca9a4351a026cd0e05ee3907&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A7777%2Fcallback&scope=user-read-currently-playing
# "https://accounts.spotify.com/authorize?" + encode_headers(auth_headers
