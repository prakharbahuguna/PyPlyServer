from flask import Flask
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
file_handler = RotatingFileHandler("/opt/repo/ROOT/log.txt")
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

with open('test1.txt', 'a') as the_file:
    the_file.write('TEST')

@app.route('/')
def hello_world():
    with open('test2.txt', 'a') as the_file:
        the_file.write('TEST')
    return 'Hello World!'

@app.route('/spotifyToken')
def spotify_token():
    with open('test3.txt', 'a') as the_file:
        the_file.write('TEST')
    return 'TOKEN'

if __name__ == '__main__':
    app.run()