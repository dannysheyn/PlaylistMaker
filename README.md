# PlaylistMaker
This app will take a playlist from Apple music and turn it into a spotify playlist


<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PlayList Maker</title>
  <!--<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.1/css/bulma.min.css"> 
  <link rel="stylesheet" href="{{ url_for('static', filename='/node_modules/bulma/css/bulma.css')}}">
  <link rel="stylesheet" href="{{ url_for('static', filename='main.css') }}">
  <link rel="stylesheet" href="{{ url_for('static', filename='debug.css')}}">

-->
  <link rel="stylesheet" href="{{ url_for('static', filename='css/mystyles.css')}}">
  <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
</head>
<body>
      <section class="hero is-fullheight is-primary is-bold">
              <section class="section">
                <div class="column is-9 is-offset-1">
                <div class="card">
                  <div class="content">
                    <section class="section">
                        <h1 class="is-size-2">Playlist Exchange</h1>
                            <section class="section">
                                <p class="is-size-4">
                                    Convert an Apple Music playlist to a Spotify Playlist using only an Apple Music playlisyt URL!<br>
                                </p>
                                <p>
                                    How does it work?<br>
                                    Sign in via Spotify.<br>
                                    Select the new playlist name, description, privacy.<br>
                                    enter URL, Select the songs you want and make yourself a new playlist! 
                                </p>
                                <a class="button is-primary" href={{auth_url}}>Sign in using spotify</a>
                            </section>
                            <section class="section">
                                <p>Here is a walkthrough of using this website.</p>
                                <br>
                                <img src="resources/demo.gif"  width="600px" height="400px"><br>
                            </section>                 
                      </section>
                  </div>
                </div>
            </section>
            </div>
        <div class="hero-foot">
              <p class="has-text-centered mb-1 has-text-black">
                This website was created by Daniel.S. Please visit the about page for more infomation.
              </p>
        </div>
      </section>
  <script type="text/javascript" src="static/index.js" charset="utf-8"></script>
</body>
</html>

