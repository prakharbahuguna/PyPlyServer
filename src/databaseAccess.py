import peewee
from peewee import *

db = MySQLDatabase('PyPly', user='root',passwd='gyt3xbsASa', host='mariadb92493-pyply.j.layershift.co.uk')
db.connect()

class User(peewee.Model):
    partyId = peewee.IntegerField()
    mobileNumber = peewee.CharField()
    credit = peewee.IntegerField()

    class Meta:
        database = db

class Playlist(peewee.Model):
    spotifyId = peewee.CharField()
    partyId = peewee.IntegerField()
    votes = peewee.IntegerField()
    voteskips = peewee.IntegerField()

    class Meta:
        database = db

class UserLikes(peewee.Model):
    userID = peewee.CharField()
    artistURI = peewee.CharField()

    class Meta:
        database = db

#UserLikes.create_table()

# User.drop_table()
# User.create_table()
# Playlist.update()
# myUser = User.create(partyId = 1, mobileNumber = 2)
# myUser.save()

#for user in User.filter(partyId = 1):
#    print user.mobileNumber