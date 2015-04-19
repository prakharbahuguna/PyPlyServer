__author__ = 'georgevanburgh'

import zmq
import json
import time
import threading
from databaseAccess import *


TOPIC_PORT = "5556"
LISTEN_PORT = "5557"
context = zmq.Context()
topicSocket = context.socket(zmq.PUB)
listenSocket = context.socket(zmq.SUB)

def init():
    topicSocket.bind("tcp://*:%s" % TOPIC_PORT)
    listenSocket.bind("tcp://*:%s" % LISTEN_PORT)

def isInit():
    return topicSocket is not None and listenSocket is not None

def partyPauseTrack(partyId):
    topicSocket.send_string("{0} pause".format(partyId))

def sendPlaylistToParty(partyID):
    playlistToSend = Playlist.select().where(Playlist.partyId == partyID).order_by(Playlist.votes)
    listToSend = []

    for song in playlistToSend:
        listToSend.append(song.spotifyId)

    jsonList = json.dumps(listToSend, separators=(',', ':'))
    print jsonList
    #topicSocket.send_string("{} loadPlaylist {}".format(partyID, jsonList))

def voteSkip(partyId):
    topicSocket.send_string("{} voteskip".format(partyId))

class zmqThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        init()
    def run(self):
        while True:
            sendPlaylistToParty("1234")
            print "Sent message!"
            time.sleep(10)

if __name__ == "__main__":
    while True:
        sendPlaylistToParty("1234")
        print "Sent message!"
        time.sleep(10)