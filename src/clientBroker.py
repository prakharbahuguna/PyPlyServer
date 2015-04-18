__author__ = 'mattakerman'

import json

class ClientBroker:
    def __init__(self):
        return

    def marshalSpotifyURIsToJSON(self, spotifyURIs):
        return json.dumps(spotifyURIs, separators=(',', ':'))

