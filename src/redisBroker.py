__author__ = 'georgevanburgh'

from redis import Redis
from rq import Worker, Queue, Connection
import json
import time
from databaseAccess import *




class RedisBroker:
    topicName = "party"

    def __init__(self):
        self.redisClient = Redis(host="redis92559-pyply.j.layershift.co.uk", password="O3KcaI9RRj")

    def partyPauseTrack(self, partyId):
        message = "{0} pause".format(partyId)
        print "Pushing {}".format(message)
        self.redisClient.rpush(self.topicName, message)

    def sendPlaylistToParty(self, partyID):
        playlistToSend = Playlist.select().where(Playlist.partyId == partyID).order_by(Playlist.votes)
        listToSend = []

        for song in playlistToSend:
            listToSend.append(song.spotifyId)

        jsonList = json.dumps(listToSend, separators=(',', ':'))
        print jsonList
        self.redisClient.rpush(self.topicName, jsonList)

    def voteSkip(self, partyId):
        self.redisClient.rpush(self.topicName, "{} voteskip".format(partyId))

if __name__ == "__main__":
    redisTest = RedisBroker()
    redisTest.sendPlaylistToParty(1234)