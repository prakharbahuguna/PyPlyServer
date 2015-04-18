from flask import Flask, redirect, request, url_for, session
from flask_oauthlib.client import OAuth, OAuthException
import logging
from logging.handlers import RotatingFileHandler
from apiUtils import APIUtils
from databaseAccess import Playlist
import smsBroker
import json
from userLikesBroker import UserLikesBroker
import spotipy

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

oauth = OAuth(app)
apiUtils = APIUtils()

SPOTIFY_CLIENT_ID = apiUtils.getSpotifyClientID()
SPOTIFY_SECRET = apiUtils.getSpotifyClientSecret()

FACEBOOK_APP_ID = apiUtils.getFacebookID()
FACEBOOK_APP_SECRET = apiUtils.getFacebookSecret()

#file_handler = RotatingFileHandler("/opt/repo/ROOT/log.txt")
#file_handler.setLevel(logging.WARNING)
#app.logger.addHandler(file_handler)

smsbroker = smsBroker.SmsBroker()

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

@app.route('/SMS')
def SMSReceived():
    # Get request fields
    message = request.args.get('Body')
    number = request.args.get('From')
    processedMessage = smsbroker.processTextMessage(number, message)
    return processedMessage

@app.route('/')
def index():
    return "Hello"

@app.route('/spotify')
def spotifyindex():
    return redirect(url_for('login'))


@app.route('/spotifylogin')
def spotifylogin():
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

    session['spotify_token'] = (resp['access_token'], '')
    userdetails = spotify.get('https://api.spotify.com/v1/me')
    if userdetails is None:
        return 'Could not find account'
    return 'Logged in as id={0} followers={1} redirect={2}'.format(
        userdetails.data['id'],
        userdetails.data['followers'],
        request.args.get('next')
    )


@spotify.tokengetter
def get_spotify_oauth_token():
    return session.get('spotify_token')

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ['email', 'user_likes'] }
)

@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('facebook_token')

@app.route('/facebooklogin')
def facebooklogin():
    callback = url_for(
        'facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    print callback
    return facebook.authorize(callback=callback)

@app.route('/facebook-authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        return redirect(next_url)

    session['facebook_token'] = (
        resp['access_token'],
    )

    userResults = facebook.get("me")
    uID = userResults.data['id']

    musicResults = facebook.get("me/music")
    data = musicResults.data['data']

    artistNames = []

    for item in data:
        if item['category'] == 'Musician/band':
            artistNames.append(item['name'])

    userLikesBroker = UserLikesBroker()
    userLikesBroker.saveUserLikes(artists=artistNames, uID=uID)

    return redirect(next_url)


@app.route('/party/<partyId>')
def party(partyId):
    if Playlist.select().where(Playlist.partyId == partyId).count() > 0:
        return json.dumps({'success': True, 'playlist_prompt': False}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': True, 'playlist_prompt': True}), 200, {'ContentType': 'application/json'}


@app.route('/playlist/<party>/<plist>')
def playlist(party, plist):
    sp = spotipy.Spotify(auth=get_spotify_oauth_token())
    userId = sp.current_user().data['id']

    results = sp.user_playlist_tracks(user=userId, playlist_id=plist, fields='tracks(items(track(uri)))')['tracks']
    for track in results:
        trackUri = track['items']['track']['uri']
        newPlaylist = Playlist.create(spotifyId=trackUri, partyId=party, votes=0, voteskips=0)
        newPlaylist.save()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run()
