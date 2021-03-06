__author__ = 'matt'

from databaseAccess import *
import spotipy

class UserLikesBroker():

    def __init__(self):
        self.spotify = spotipy.Spotify()

    def saveUserLikes(self, artists, uID):
        print uID
        try:
            UserLikes.get(UserLikes.userID == uID)
        except:
            artistURIs = self.getArtistURIs(artists)

            for uri in artistURIs:
                userlike = UserLikes.create(userID=uID,artistURI=uri)
                userlike.save()

    def getArtistURIs(self, artists):
        artistURIs = []

        for artist in artists:
            results = self.spotify.search(q='artist:' + artist, type='artist')
            if len(results) > 0:
                artistsData = results['artists']
                if len(artistsData) > 0:
                    if len(artistsData['items']) > 0:
                        artistInfo = artistsData['items'][0]
                        artistURIs.append(artistInfo["uri"])

        return artistURIs