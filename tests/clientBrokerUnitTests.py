__author__ = 'matt'

import unittest
from clientBroker import ClientBroker
import json

class ClientBrokerUnitTests(unittest.TestCase):
    def test_marshal_spotify_uris_to_json(self):
        clientBroker = ClientBroker()
        spotifyURIs = ["uri1", "uri2", "uri3", "uri4"]
        jsonArray = clientBroker.marshalSpotifyURIsToJSON(spotifyURIs)
        self.assertEqual(jsonArray, json.dumps(spotifyURIs))

if __name__ == '__main__':
    unittest.main()
