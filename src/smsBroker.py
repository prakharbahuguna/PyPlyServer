__author__ = 'georgevanburgh'

from databaseAccess import *

class smsBroker():

    def processTextMessage(self, givenNumber, givenMessage):
        messageParts = givenMessage.split()
        verb = messageParts[0].lower()
        arguments = None
        if len(messageParts) > 1:
            arguments = messageParts[1]
        if verb == 'register':
            partyId = arguments
            user = None
            try:
                user = User.get(User.mobileNumber == givenNumber)
            except User.DoesNotExist:
                user = None
            # If we've already got the correct details - nothing needs to be done
            if user and user.partyId == partyId:
                pass
            # If the user exists without the correct details - delete him/her
            if user:
                user.delete()
            # Now insert a new user entry
            newUser = User.create(mobileNumber = givenNumber, partyId = partyId)
            newUser.save()



if __name__ == '__main__':
    underTest = smsBroker()
    underTest.processTextMessage("07903120756", "reGister 1234")