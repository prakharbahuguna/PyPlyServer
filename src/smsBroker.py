__author__ = 'georgevanburgh'

from databaseAccess import *
import redisBroker
import spotipy
from twilioBroker import TwilioBroker

class SmsBroker():

    def __init__(self):
        self.mySpotipy = spotipy.Spotify()
        self.twilioBroker = TwilioBroker()
        if not redisBroker.isInit():
            redisBroker.init()

    def processTextMessage(self, givenNumber, givenMessage):
        messageParts = givenMessage.split()
        verb = messageParts[0].lower()
        arguments = None
        processedMessage = ""
        if len(messageParts) > 1:
            arguments = messageParts[1]
        if verb == 'register':
            processedMessage = self.registerUser(givenNumber, arguments)
        if verb == 'vote':
            processedMessage = self.incrementVoteCount(givenNumber, arguments)
        if verb == 'playlist':
            processedMessage = self.textPlaylistToUser(givenNumber)
        if verb == 'pause':
            processedMessage = self.pauseParty(givenNumber)
        if verb == 'voteskip':
            processedMessage = self.skipCurrentTrack(givenNumber)
        if verb == 'preview':
            processedMessage = self.sendTrackPreview(givenNumber, arguments)
        if not processedMessage:
            processedMessage = "Placeholder message"
        return processedMessage

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
        user = self.getUser(phoneNumber)
        # If we've already got the correct details - nothing needs to be done
        if user and user.partyId == int(partyId):
            pass
        # If the user exists without the correct details - delete him/her
        if user:
            user.delete_instance()
        # Now insert a new user entry
        newUser = User.create(mobileNumber = phoneNumber, partyId = partyId, credit=10)
        newUser.save()
        return "You have been successfully registered for the party"

    def decrementUserCredit(self, phoneNumber):
        # Mhhhh all this user stuff needs cleaning up
        user = self.getUser(phoneNumber)
        if user and user.credit > 0:
            user.credit -= 1
            return True
        return False

    def incrementVoteCount(self, givenNumber, givenSong):
        if self.decrementUserCredit(givenNumber):
            partyId = self.getPartyId(givenNumber)
            if partyId is None:
                return "You must register for a party before you can vote on its playlist"
            playlistEntry = Playlist.get(partyId = partyId, id = givenSong)
            playlistEntry.votes += 1
            playlistEntry.save()
            redisBroker.sendPlaylistToParty(partyId)
            return "Thank you for your vote"
        else:
            return "Sorry, you have insufficient credit to vote"

    def pauseParty(self, givenNumber):
        partyId = self.getPartyId(givenNumber)
        redisBroker.partyPauseTrack(partyId)

    def skipCurrentTrack(self, givenNumber):
        partyId = self.getPartyId(givenNumber)
        redisBroker.voteSkip(partyId)

    def getUser(self, givenNumber):
        try:
            user = User.get(mobileNumber = givenNumber)
        except User.DoesNotExist:
            return None
        return user

    def getPartyId(self, givenNumber):
        user = self.getUser(givenNumber)
        if not user:
            return None
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
     underTest = SmsBroker()
     underTest.sendTrackPreview('07432142620', '4')