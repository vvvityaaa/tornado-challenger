import mongoengine #object-relational mapper for MongoDB database

class ChallengePoint(mongoengine.EmbeddedDocument):
    '''
    Point of challenge. Has embedded relation. Does not have to be imported
    to challenge_manager.py file.
    '''
    title = mongoengine.StringField(required = True)
    key = mongoengine.IntField(unique = True)
    done = mongoengine.StringField()
    required_time = mongoengine.IntField()
    meta = {'allow_inheritance': False}
    
class Challenge(mongoengine.Document):
    '''
    Model in the database, which describes one challenge with it's points.
    Has to be imported to challenge_manager.py file.
    '''
    header = mongoengine.StringField(max_length=150, required = True)
    url = mongoengine.StringField(max_length = 50, required = True)
    date_start = mongoengine.DateTimeField()
    date_end = mongoengine.DateTimeField()
    points = mongoengine.EmbeddedDocumentListField(ChallengePoint)
    meta = {'allow_inheritance': False}
    