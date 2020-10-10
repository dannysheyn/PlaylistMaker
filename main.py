from flask import Flask, render_template, request, session, redirect, Response
import uuid
import os
import spotipy
import requests

app = Flask(__name__)
app.secret_key = 'hiiiii'
site_url = 'http://127.0.0.1:5000/'
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
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='playlist-modify-public', redirect_uri='http://127.0.0.1:5000/',
                                               show_dialog=True)
    if not auth_manager.get_cached_token():
        resp = Response('Some error has accord')
        resp.status_code = 500
        return resp
    song_list_dict = request.get_json(force=True)
    song_list = song_list_dict['SongList']
    try:
        sp_user = spotipy.Spotify(auth_manager=auth_manager)
        # song_uri_list = get_song_uri(sp_user,song_list)
        # song_uri_list = [search_json['tracks']['items'][0]['uri'] for search_json in song_uri_list if search_json['tracks']['items'].__len__() != 0]
        # playlist_created = sp_user.user_playlist_create(user=sp_user.me()['id'],name=song_list_dict['PlaylistName'], public=song_list_dict['IsPrivate'],collaborative=False,description=song_list_dict['Description'])
        # sp_user.playlist_add_items(playlist_created['id'],song_uri_list)
        resp = Response(response='Playlist moved successfully')
        resp.status_code = 200
        return resp
    except:
        resp = Response('Some error has accord')
        resp.status_code = 500
        return resp


@app.route('/request_html')
def request_html():
    url = request.args.get('url')
    requested_html = requests.get(url).text
    resp = Response(requested_html)
    resp.headers['Access-Control-Allow-Origin'] = site_url
    return resp


@app.route('/sign_out')
def sign_out():
    os.remove('.cache')
    session.clear()
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove('.cache')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')


@app.route('/')
def index():
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='playlist-modify-public', redirect_uri='http://127.0.0.1:5000/',
                                               show_dialog=True)

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.get_cached_token():
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return render_template('home.html', auth_url=auth_url)

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

init:
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
album_names = driver.find_elements_by_class_name('song-album-wrapper')
album_names = [str(i.text) for i in p]
album_names = list(filter(lambda x: x != '', album_names))
song_artist = driver.find_elements_by_class_name('song-album-wrapper')
song_artist = [str(i.text) for i in song_artist]
song_artist = [i.split('\n') for i in song_artist]
song_artist_album = [artist[i].append(album_names[i] for i in range(artist.__len__())]

# sp = spotipy.Spotify(auth=Client_ID,auth_manager=SpotifyOAuth(scope=scope))
# spotify.search(q='let it happen',type='track', limit=1)

spotipy = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='9cba5f9abba44b628cfa2e5aadaf1994',
                                                            client_secret='c16f4c51858545c29dc0affb3bd327a1'))

'''
