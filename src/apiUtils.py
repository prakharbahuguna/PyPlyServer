__author__ = 'matt'

import json
import spotipy
import spotipy.util as util
import sys
import os

datapath = os.path.dirname(os.path.realpath(__file__)) + '/data'
sys.path.insert(0, datapath)
DATA_PATH = os.path.join(datapath, "API_info")

class APIUtils():

    def __init__(self):
        self.apiInfo = json.load(open(DATA_PATH))

    def getAPI_JSON(self):
        return self.apiInfo

    def getSpotifyClientID(self):
        return self.apiInfo["spotifyClientID"]

    def getSpotifyClientSecret(self):
        return self.apiInfo["spotifyClientSecret"]

    def getSpotifyRedirectURI(self):
        return self.apiInfo["spotifyRedirectURI"]

    def getSpotifyTokenURL(self):
        return self.apiInfo["spotifyTokenURL"]

    def getSpotifyToken(self, user):
        return util.prompt_for_user_token(username=user, scope="playlist-modify-public", client_id=self.apiInfo["spotifyClientID"],
                                          client_secret=self.apiInfo["spotifyClientSecret"], redirect_uri=self.apiInfo["spotifyRedirectURI"])