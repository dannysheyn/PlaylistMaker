import pymongo
from user import User
from time import gmtime, strftime

'''
MONGODB_DB = 'PlaylistExchange'
MONGODB_COLLECTTION = 'UserData'
client = pymongo.MongoClient('mongodb+srv://Dadmin:<password>@cluster0.miqhi.mongodb.net/test')
db = client[MONGODB_DB]
col = db[MONGODB_COLLECTTION]
'''


class MongoUserHandler:
    def __init__(self):
        self.MONGODB_DB = 'PlaylistExchange'
        self.MONGODB_COLLECTION = 'UserData'
        self.MONGODB_SESSION = 'UserSession'
        self.client = pymongo.MongoClient('mongodb+srv://Dadmin:4yjqRA9z7CduBMD@cluster0.miqhi.mongodb.net/test')
        self.db = self.client[self.MONGODB_DB]
        self.db_collection = self.db[self.MONGODB_COLLECTION]

    def find_and_update_user(self, spotify_user, number_tracks_added):
        found_user = self.find_user_by_parameter('spotify_id', spotify_user.me()['id'])
        try:
            if found_user is not None:
                self.update_user_tracks(found_user['_id'], number_tracks_added)
            else:
                new_user = User(spotify_user, playlist_converted_count=1,
                                playlist_added_time=[self.getCurrentTime()],
                                total_songs_converted=number_tracks_added)
                self.db_collection.insert_one(new_user.to_json())
        except Exception as e:
            print("type error: " + str(e))

    def update_user_tracks(self, user_id, number_tracks_added):
        filter_key = '_id'
        inc_key = '$inc'
        add_date_key = '$addToSet'
        self.db_collection.find_one_and_update({filter_key: user_id}, {inc_key: dict(playlist_converted_count=1,
                                                                                     total_songs_converted=number_tracks_added),

                                                                       add_date_key: {
                                                                           'playlist_converted_datetime': self.getCurrentTime()}})
        return

    def find_user_by_parameter(self, parameter, user_query):
        return self.db_collection.find_one({parameter: user_query})

    def getCurrentTime(self):
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())

    '''
       db.restaurant.updateOne(
       { "name" : "Pizza Rat's Pizzaria" },
       { $inc: { "violations" : 3}, $set: { "Closed" : true } },
       { w: "majority", wtimeout: 100 }
       
       
     >> datetime.strptime("2010-06-04 21:08:12", "%Y-%m-%d %H:%M:%S")
datetime.datetime(2010, 6, 4, 21, 8, 12)
    '''
