__author__ = 'georgevanburgh'

from databaseAccess import *
import zeroMqBroker
import spotipy
from twilioBroker import TwilioBroker

class smsBroker():

    def __init__(self):
        self.mySpotipy = spotipy.Spotify()
        self.twilioBroker = TwilioBroker()
        if not zeroMqBroker.isInit():
            zeroMqBroker.init()

    def processTextMessage(self, givenNumber, givenMessage):
        messageParts = givenMessage.split()
        verb = messageParts[0].lower()
        arguments = None
        if len(messageParts) > 1:
            arguments = messageParts[1]
        if verb == 'register':
            self.registerUser(givenNumber, arguments)
        if verb == 'vote':
            self.incrementVoteCount(givenNumber, arguments)
        if verb == 'playlist':
            self.textPlaylistToUser(givenNumber)
        if verb == 'pause':
            self.pauseParty(givenNumber)
        if verb == 'voteskip':
            self.skipCurrentTrack(givenNumber)
        if verb == 'preview':
            self.sendTrackPreview(givenNumber, arguments)

    def textPlaylistToUser(self, givenNumber):
        userParty = self.getPartyId(givenNumber)
        playlist = Playlist.select().where(Playlist.partyId == userParty).order_by(Playlist.votes)
        toText = ""
        for item in playlist:
            #TODO: Convert Spotify URIs to Artist:Songname combos
            trackInfo = self.mySpotipy.track(item.spotifyId)
            toText += "{0}: {1} - {2}\n".format(item.get_id(), trackInfo['name'], trackInfo['artists'][0]['name'])
        print toText

    def registerUser(self, phoneNumber, partyId):
        user = None
        try:
            user = User.get(User.mobileNumber == phoneNumber)
        except User.DoesNotExist:
            user = None
        # If we've already got the correct details - nothing needs to be done
        if user and user.partyId == partyId:
            pass
        # If the user exists without the correct details - delete him/her
        if user:
            user.delete()
        # Now insert a new user entry
        newUser = User.create(mobileNumber = phoneNumber, partyId = partyId)
        newUser.save()

    def incrementVoteCount(self, givenNumber, givenSong):
        partyId = self.getPartyId(givenNumber)
        playlistEntry = Playlist.get(partyId = partyId, id = givenSong)
        playlistEntry.votes += 1
        playlistEntry.save()

    def pauseParty(self, givenNumber):
        partyId = self.getPartyId(givenNumber)
        zeroMqBroker.partyPauseTrack(partyId)

    def skipCurrentTrack(self, givenNumber):
        partyId = self.getPartyId(givenNumber)
        zeroMqBroker.voteSkip(partyId)

    def getPartyId(self, givenNumber):
        user = User.get(mobileNumber = givenNumber)
        return user.partyId

    def getSpotifyIdFromTrackId(self, givenTrackId):
        song = Playlist.get(id = givenTrackId)
        return song.spotifyId

    def sendTrackPreview(self, givenNumber, givenTrackId):
        spotifyId = self.getSpotifyIdFromTrackId(givenTrackId)
        spotifyData = self.mySpotipy.track(spotifyId)
        trackUrl = spotifyData['preview_url']
        self.twilioBroker.playMp3ToUser(givenNumber, trackUrl)



if __name__ == '__main__':
     underTest = smsBroker()
     underTest.sendTrackPreview('07432142620', '4')