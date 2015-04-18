from flask import Flask, redirect, request, url_for, session
from flask_oauthlib.client import OAuth, OAuthException
import logging
from logging.handlers import RotatingFileHandler
from apiUtils import APIUtils

app = Flask(__name__)
app.debug = True
oauth = OAuth(app)
apiUtils = APIUtils()

app = Flask(__name__)
file_handler = RotatingFileHandler("/opt/repo/ROOT/log.txt")
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

spotify = oauth.remote_app(
    'spotify',
    consumer_key=apiUtils.getSpotifyClientID(),
    consumer_secret=apiUtils.getSpotifyClientSecret(),
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
    me = spotify.get('/me')
    return 'Logged in as id={0} name={1} redirect={2}'.format(
        me.data['id'],
        me.data['name'],
        request.args.get('next')
    )


@spotify.tokengetter
def get_spotify_oauth_token():
    return session.get('oauth_token')


@app.route('/sms', methods=['POST'])
def sms():
    print request
    print "SDSADSD"
    print request.data
    print "BOOP"
    print
    #message = request.args.get('Body').split(" ")
    #message[0] = message[0].lower()
    #sms = SMS(givenMessage=message, givenNumber=request.args.get('From'))
    return

if __name__ == '__main__':
    app.run()