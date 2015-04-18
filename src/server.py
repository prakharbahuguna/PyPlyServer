from flask import Flask, redirect, request, url_for, session
from flask_oauthlib.client import OAuth, OAuthException
import logging
from logging.handlers import RotatingFileHandler
from apiUtils import APIUtils

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

oauth = OAuth(app)
apiUtils = APIUtils()

SPOTIFY_CLIENT_ID=apiUtils.getSpotifyClientID()
SPOTIFY_SECRET=apiUtils.getSpotifyClientSecret()

file_handler = RotatingFileHandler("/opt/repo/ROOT/log.txt")
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

spotify = oauth.remote_app(
    'spotify',
    consumer_key=SPOTIFY_CLIENT_ID,
    consumer_secret=SPOTIFY_SECRET,
    # Change the scope to match whatever it us you need
    # list of scopes can be found in the url below
    # https://developer.spotify.com/web-api/using-scopes/
    request_token_params={'scope': 'user-read-email'},
    base_url='https://accounts.spotify.com',
    request_token_url=None,
    access_token_url='/api/token',
    authorize_url='https://accounts.spotify.com/authorize'
)

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/spotify')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    callback = url_for(
        'spotify_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return spotify.authorize(callback=callback)


@app.route('/login/authorized')
def spotify_authorized():
    resp = spotify.authorized_response()
    if resp is None:
        return 'Access denied: reason={0} error={1}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: {0}'.format(resp.message)

    session['oauth_token'] = (resp['access_token'], '')
    userdetails = spotify.get('https://api.spotify.com/v1/me')
    if userdetails is None:
        return 'Could not find account'
    return 'Logged in as id={0} name={1} redirect={2}'.format(
        userdetails.data['id'],
        userdetails.data['product'],
        request.args.get('next')
    )

@spotify.tokengetter
def get_spotify_oauth_token():
    return session.get('oauth_token')


app.route('/SMS')
def SMSReceived():
    # Get request fields
    message = request.args.get('Body').split(" ")
    message = message[0].lower()
    print message
    return 200

if __name__ == '__main__':
    app.run()