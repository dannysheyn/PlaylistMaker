import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


class SpotifyAdapter():
    def __init__(self):
        self.spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(client_id='9cba5f9abba44b628cfa2e5aadaf1994',
                                                            client_secret='c16f4c51858545c29dc0affb3bd327a1'))


        def search_all_tracks(self, song_artist_list):
            """
            querys all songs in the list given
            """
            uri_track_list = [
                self.spotify.search(q='track:%{} artist:%{}'.format(song_artist_list[i]['song'],
                                                            song_artist_list[i]['artist']
                                                            ), type='track', limit=1)
                for i in range(song_artist_list.__len__())
            ]