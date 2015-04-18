__author__ = 'georgevanburgh'

import zmq


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

if __name__ == "__main__":
    test = zeroMqBroker()
    while True:
        test.partySkipTrack("house1")