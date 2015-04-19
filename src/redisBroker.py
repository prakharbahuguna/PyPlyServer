__author__ = 'georgevanburgh'

import json

from redis import Redis

from databaseAccess import *


class RedisBroker:
    topicName = "party"

    def __init__(self):
        self.redisClient = Redis(host="redis92559-pyply.j.layershift.co.uk", password="O3KcaI9RRj")

    def partyTogglePause(self, partyId):
        message = "{0} togglePause".format(partyId)
        print "Pushing {}".format(message)
        self.redisClient.rpush(self.topicName, message)

    def sendPlaylistToParty(self, partyID):
        playlistToSend = Playlist.select().where(Playlist.partyId == partyID).order_by(Playlist.votes.desc())
        listToSend = []

        for song in playlistToSend:
            listToSend.append(song.spotifyId)

        jsonList = json.dumps(listToSend, separators=(',', ':'))
        print jsonList
        self.redisClient.rpush(self.topicName, "loadPlaylist {}".format(jsonList))

    def voteSkip(self, partyId):
        self.redisClient.rpush(self.topicName, "skipVote".format(partyId))

if __name__ == "__main__":
    redisTest = RedisBroker()
    redisTest.sendPlaylistToParty(1234)