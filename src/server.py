from flask import Flask
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
file_handler = RotatingFileHandler("log.txt")
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/spotifyToken')
def spotify_token():
    return 'TOKEN'

if __name__ == '__main__':
    app.run()