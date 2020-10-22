import spotipy
import json
from time import gmtime, strftime


class User:
    def __init__(self, spotify_user, playlist_converted_count=0, playlist_added_time=[], total_songs_converted=0):
        self.spotify_id = spotify_user.me()['id']
        self.spotify_uri = spotify_user.me()['uri']
        self.spotify_display_name = spotify_user.me()['display_name']
        self.spotify_href = spotify_user.me()['href']
        self.spotify_type = spotify_user.me()['type']
        self.spotify_user_link = spotify_user.me()['external_urls']['spotify']
        self.playlist_converted_count = playlist_converted_count
        self.playlist_converted_datetime = playlist_added_time
        self.total_songs_converted = total_songs_converted

    def to_json(self):
        return json.loads(json.dumps(self.__dict__))

    def update_user(self, track_num_added):
        self.total_songs_converted += track_num_added
        self.playlist_converted_count += 1
        self.playlist_converted_datetime.append(strftime("%Y-%m-%d %H:%M:%S", gmtime()))


'''
User:
{
    SpotifyId: string,
    PlaylistConvertCount: int,
    PlatlistConvertDateTimes: [DateTime]
    TotalNumberOfSongsConverted : int
}

spotify.me()['id']
spotify.me()['uri']
spotify.me()['type']
ddd = {'spotify_id' : 'sheynan', 'spotify_uri' : 'someTryHref',
 'spotify_display_name' : 'sheynan','spotify_type' : 'user', 'playlist_converted_count': 0,
'playlist_converted_datetime' : [] ,'total_songs_converted' : 0 }


'''
