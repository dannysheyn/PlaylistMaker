"""

TODO: make a user and db system that counts the number of playlist transfers.

"""
from flask_session import Session

from flask import Flask, render_template, request, session, redirect, Response, send_file
import uuid
import os
import spotipy
import requests
from mongouserhandler import MongoUserHandler
from flask_cors import CORS, cross_origin

'''
PlaylistExchange
UserData
SESSION_TYPE = 'mongodb'
'''
DataBaseHandler = MongoUserHandler()
app = Flask(__name__)
site_url = 'http://127.0.0.1:5000/'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
app.config.from_object(__name__)
Session(app)
CORS(app)
APP_SCOPE = "playlist-read-private, playlist-modify-public"



caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def session_cache_path():
    return caches_folder + session.get('uuid')


def get_song_uri(spotify, song_artist_list):
    return [spotify.search(song_artist_list[i], limit=1, offset=0, type='track', market=None) for i in
            range(song_artist_list.__len__())]


@app.route('/index', methods=['POST', 'GET'])
def home_page():
    return render_template('Test.html', header='header.html')


@app.route('/find_songs', methods=['POST'])
def find_songs():
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=APP_SCOPE, redirect_uri='http://127.0.0.1:5000/',
                                               cache_path=session_cache_path(),
                                               show_dialog=True)
    if not auth_manager.get_cached_token():
        resp = Response('Some error has accord')
        resp.status_code = 500
        return resp
    song_list_dict = request.get_json(force=True)
    if song_list_dict['PlaylistName'] == "":
        song_list_dict['PlaylistName'] = "Playlist By MakeAList"
    song_list = song_list_dict['SongList']
    try:
        sp_user = spotipy.Spotify(auth_manager=auth_manager)
        song_uri_list = get_song_uri(sp_user, song_list)
        song_uri_list = [search_json['tracks']['items'][0]['uri'] for search_json in song_uri_list if
                         search_json['tracks']['items'].__len__() != 0]
        playlist_created = sp_user.user_playlist_create(user=sp_user.me()['id'], name=song_list_dict['PlaylistName'],
                                                        public=song_list_dict['IsPrivate'], collaborative=False,
                                                        description=song_list_dict['Description'])
        sp_user.playlist_add_items(playlist_created['id'], song_uri_list)
        DataBaseHandler.find_and_update_user(sp_user, song_uri_list.__len__())
        resp = Response(response=playlist_created['external_urls']['spotify'])
        resp.status_code = 200
        return resp
    except Exception as e:
        print("type error: " + str(e))
        resp = Response('"type error: " + str(e)')
        resp.status_code = 500
        return resp


@app.route('/request_html')
def request_html():
    url = request.args.get('url')
    requested_html = requests.get(url).text
    resp = Response(requested_html)
    resp.headers['Access-Control-Allow-Origin'] = site_url
    return resp

@app.route('/about')
def about():
    spotify = None
    spotify = None
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())
    
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=APP_SCOPE, redirect_uri='http://127.0.0.1:5000/',
                                               cache_path=session_cache_path(),
                                               show_dialog=True)

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/about')

    if not auth_manager.get_cached_token():
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return render_template('about.html',spotify=spotify , auth_url=auth_url)

    # Step 4. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    
    return render_template('about.html',spotify=spotify)


@app.route('/sign_out')
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')

@app.route('/resources/demo.gif')
def gif():
     return send_file('resources/demo.gif', mimetype='image/gif')

@app.route('/')
def index():
    spotify = None
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())
    
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=APP_SCOPE, redirect_uri='http://127.0.0.1:5000/',
                                               cache_path=session_cache_path(),
                                               show_dialog=True)

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.get_cached_token():
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return render_template('home.html',spotify=spotify , auth_url=auth_url)

    # Step 4. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    return render_template('userhome.html', spotify=spotify)


if __name__ == '__main__':
    app.run(debug=True)

'''
https://music.apple.com/il/playlist/wmai-idan/pl.u-RRbVYr2I3oNk0NK
'https://music.apple.com/il/playlist/wmai-idan/pl.u-RRbVYr2I3oNk0NK'

x = spotify.current_user_playlists()
y = spotify.user_playlist_create(user=spotify.me()['id'],name='TryPlaylist', public=True,collaborative=False,description='This playlist was originated from an apple music playlist')

# sp = spotipy.Spotify(auth=Client_ID,auth_manager=SpotifyOAuth(scope=scope))
# spotify.search(q='let it happen',type='track', limit=1)

spotipy = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='9cba5f9abba44b628cfa2e5aadaf1994',
                                                            client_secret='c16f4c51858545c29dc0affb3bd327a1'))

'''
