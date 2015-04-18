__author__ = 'matt'

import json
import unittest
from apiUtils import APIUtils
import spotipy
import spotipy.util as util

scope = 'playlist-modify-public'

class APIUtilsUnittests(unittest.TestCase):

    def test_spotify_api_info(self):
        apiUtils = APIUtils()
        apiInfo = json.load(open('data/API_info'))

        self.assertEqual(apiInfo, apiUtils.getAPI_JSON(), "Unexpected JSON file")

        spotifyClientID = apiInfo["spotifyClientID"]
        spotifyClientSecret = apiInfo["spotifyClientSecret"]
        spotifyRedirectURI = apiInfo["spotifyRedirectURI"]

        self.assertEqual(spotifyClientID, apiUtils.getSpotifyClientID(), 'Unexpected Spotify Client ID')
        self.assertEqual(spotifyClientSecret, apiUtils.getSpotifyClientSecret(), 'Unexpected Spotify Client Secret')
        self.assertEqual(spotifyRedirectURI, apiUtils.getSpotifyRedirectURI(), 'Unexpected Spotify Redirect URI')

    def test_spotify_token(self):
        apiUtils = APIUtils()

        user = 'akers99'
        spotifyToken = apiUtils.getSpotifyToken(user)
        print spotifyToken
        spotifyClientID = apiUtils.getSpotifyClientID()
        spotifyClientSecret = apiUtils.getSpotifyClientSecret()
        spotifyRedirectURI = apiUtils.getSpotifyRedirectURI()

        #self.assertEqual(spotifyToken, util.prompt_for_user_token(username=user, client_id=spotifyClientID,
        #                                                          client_secret=spotifyClientSecret,
        #                                                          redirect_uri=spotifyRedirectURI),
        #                 "Incorrect token generation")

if __name__ == '__main__':
    unittest.main()