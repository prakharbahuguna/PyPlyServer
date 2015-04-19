__author__ = 'matt'

import urllib2
from databaseAccess import Playlist, UserLikes, User
import random
import json

class PlaylistUtils:

    def __init__(self):
        self.baseURL="http://developer.echonest.com/api/v4/playlist/static?"
        self.api_key="S0QUTXZNEZ6GNVKST"
        self.lastparams="&format=json&results=20&type=artist-radio&bucket=id:spotify&bucket=tracks"

    def getArtistRadioPlaylistJSON(self,partyID):
        group = User.select().where(User.partyId == partyID)

        userLikes = None
        artistURIs = []

        for person in group:
            userLikes = UserLikes.select().where(UserLikes.userID == person.fbUserID)

            for like in userLikes:
                artistURIs.append(like.artistURI)

        if len(artistURIs) == 0:
            return {'response': {'status': {'code': '404'}}}

        artistChoices = random.sample(set(artistURIs), 5)

        requestString = self.baseURL + "api_key=" + self.api_key

        for artist in artistChoices:
            requestString += '&artist_id={0}'.format(str(artist))

        requestString += self.lastparams

        urlRequest = urllib2.Request(requestString)
        return json.load(urllib2.urlopen(urlRequest))

    def savePlaylist(self,partyID, spotifyURIs):
        for uri in spotifyURIs:
            newPlaylist = Playlist.create(spotifyId=uri, partyId=partyID, votes=0, voteskips=0)
            newPlaylist.save()

    def generatePlaylist(self,partyID):
        result = self.getArtistRadioPlaylistJSON(partyID)

        response = result['response']
        spotifyURIs = []

        if response['status']['code'] == 0:
            songs = response['songs']
            for song in songs:
                trackInfo = song['tracks'].pop(0)
                spotifyURIs.append(trackInfo['foreign_id'])

        self.savePlaylist(partyID,spotifyURIs)

#playlistUtils=PlaylistUtils()
#playlistUtils.generatePlaylist(1234)