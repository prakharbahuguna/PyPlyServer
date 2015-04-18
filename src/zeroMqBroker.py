__author__ = 'georgevanburgh'

import zmq
import json
import time

class zeroMqBroker:
    TOPIC_PORT = "5556"
    LISTEN_PORT = "5557"
    context = zmq.Context()
    topicSocket = context.socket(zmq.PUB)
    listenSocket = context.socket(zmq.SUB)

    def __init__(self):
        self.topicSocket.bind("tcp://*:%s" % self.TOPIC_PORT)
        self.listenSocket.bind("tcp://*:%s" % self.LISTEN_PORT)

    def partyPauseTrack(self, partyId):
        self.topicSocket.send_string("{0} pause".format(partyId))

    def sendPlaylistToParty(self, partyID, playlist):
        self.topicSocket.send_string("{} loadPlaylist {}".format(partyID, playlist))

if __name__ == "__main__":
    test = zeroMqBroker()
    while True:
        test.sendPlaylistToParty("house1", json.dumps(["uri1","uri2","uri3"], separators=(',', ':')))
        print "Sent message!"
        time.sleep(10)