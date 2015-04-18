__author__ = 'georgevanburgh'

import zmq
import json
import time


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

def sendPlaylistToParty(partyID, playlist):
    topicSocket.send_string("{} loadPlaylist {}".format(partyID, playlist))

def voteSkip(partyId):
    topicSocket.send_string("{} voteskip".format(partyId))

if __name__ == "__main__":
    while True:
        sendPlaylistToParty("house1", json.dumps(["uri1","uri2","uri3"], separators=(',', ':')))
        print "Sent message!"
        time.sleep(10)