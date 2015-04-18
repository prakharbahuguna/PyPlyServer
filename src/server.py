from flask import Flask, request
import requests
import base64
import json
import logging
from logging.handlers import RotatingFileHandler
import APIUtils

app = Flask(__name__)
file_handler = RotatingFileHandler("/opt/repo/ROOT/log.txt")
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

with open('/opt/repo/ROOT/test1.txt', 'a') as the_file:
    the_file.write('TEST')

@app.route('/')
def hello_world():
    with open('/opt/repo/ROOT/test2.txt', 'a') as the_file:
        the_file.write('TEST')
    return 'Hello World!'

@app.route('/spotifyToken')
def spotify_token():

    apiUtils = APIUtils()

    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": apiUtils.getSpotifyRedirectURI()
    }
    base64encoded = base64.b64encode("{}:{}".format((), apiUtils.getSpotifyClientID(), apiUtils.getSpotifyClientSecret))
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(apiUtils.getSpotifyTokenURL(), data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    return

if __name__ == '__main__':
    app.run()