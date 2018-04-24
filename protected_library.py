#!/usr/bin/env python


from cgitb import enable
enable()
from html import escape
from cgi import FieldStorage
import pymysql as db
from os import environ
from shelve import open
from http.cookies import SimpleCookie


print("Content-type: text/html")
print()

header = '''
            <header>
                <h1> Streaming </h1>
                <nav>
                  <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="streaming.py">Browse</a></li>
                    <li><a href="login.py">Login</a></li>
                    <li><a href="register.py">Register</a></li>
                  </ul>
                </nav>
            </header>'''
page = """
<main>
   <p>You do not have permission to access this page.</p>
   <ul>
       <li><a href="register.py">Register</a></li>
       <li><a href="login.py">Login</a></li>
   </ul>
</main>
   """


form_data = FieldStorage()
playlists = '<option value="my_playlist">my_playlist</option>'
playlist = ''
result = ''

try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'sid' in cookie:
            sid = cookie['sid'].value
            session_store = open('sess_' + sid, writeback=False)
            if session_store.get('authenticated'):
                username = session_store.get('username')
                try:
                    connection = db.connect('localhost', 'root', 'fordemc2', 'projects')
                    cursor = connection.cursor(db.cursors.DictCursor)

                    cursor.execute("""SELECT DISTINCT playlist_name FROM playlists 
                    where username=%s""", username)
                    if cursor.rowcount != 0:
                        playlists = ''
                        for row in cursor.fetchall():
                            playlists += '<option value="%s">%s</option>' % (row['playlist_name'], row['playlist_name'])

                    if len(form_data) != 0:
                        playlist = escape(form_data.getfirst('playlist', '')).strip()
                        cursor.execute("""SELECT * FROM music WHERE song_id in (select song_id from playlists where username = %s and playlist_name = %s)""", (username, playlist))
                        result = """
                                <audio controls source src='' type='audio/mp3' id='audioPlayer'>
                                    <p>Sorry, Your browser doesn't support HTML5</p>
                                </audio>
                                <table id='songlist'>
                                    <tr><th colspan="3">Your %s Playlist</th></tr>
                                    <tr><th>Name</th><th>Artist</th><th>Delete</th></tr>""" % playlist

                        for row in cursor.fetchall():
                            result += """<tr>
                                            <td><a href='%s'>%s</a></td>
                                            <td>%s</td>
                                            <td>       
                                                <form action="protected_remove_from_playlist.py?playlist=%s&song_id=%s" method='post'>
                                                    <input type="submit" value='Remove'/>
                                                </form>
                                            </td>
                                         </tr>""" % (row['location'], row['name'], row['artist'], playlist, row['song_id'])
                        result += '</table>'
                    cursor.close()
                    connection.close()
                except db.Error:
                    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

                header = '''
                            <header>
                                <h1> Streaming </h1>
                                <nav>
                                  <ul>
                                    <li><a href="protected_streaming.py">Browse</a></li>
                                    <li class="current"><a href="protected_library.py">Library</a></li>
                                    <li><a href="profile.py">%s</a></li>
                                    <li><a href="logout.py">Logout</a></li>
                                  </ul>
                                </nav>
                            </header>''' % username
                page = """
                        <main>
                            <h1>Welcome to your Library %s</h1>
                            <p>
                                Choose a playlist you would like to listen to and click "Open", once its open you can
                                remove music from that playlist by clicking "Remove" in the delete column.
                            </p>
                            <form action='protected_library.py' method='get'>
                                <select name="playlist">
                                %s
                                </select>
                                <input type="submit" value='Open'/>
                            </form>
                            %s
                        </main>
                        <aside>
                            <h1>Adding a new Playlist</h1>
                            <article>
                                Below you can create a playlist and add music to it, you can do this by filling in the name
                                of the playlist you want to create into the box below entitled "Create a new playlist", 
                                after you have done that you can move over to the "Add to playlist" section of the 
                                music list, on each song theres and option to choose what playlist you would like to 
                                add the song to, if you do indeed want to add that song assuming you have choosen the 
                                perferred playlist, you just click "Add". also since your in your Library, this will 
                                revert you back to the browse page.
                            </article>
                            <form action='protected_streaming.py' method='get'>
                                <label for='add_playlist'>Create a new playlist:</label>
                                <input type='text' name='new_playlist' id='add_playlist'>
                                <input type="submit" value='Add'/>
                            </form>
                        </aside>""" % (username, playlists, result)
            session_store.close()


except IOError:
    page = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'


print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta name="viewport" content="width=device-width"/>
            <meta charset="utf-8" />
            <title>Streaming</title>
            <link rel="stylesheet" href="styles.css" />
            <script src="https://code.jquery.com/jquery-2.2.0.js"></script>
        </head>
        <body>
            %s
            %s
            <script>
                    audioPlayer();
                      function audioPlayer(){
                        var currentSong = 0;
                        $('#audioPlayer')[0].src = $('#songlist tr td a')[0];
                        $('#songlist tr td a').click(function(e){
                          e.preventDefault();
                          $('#audioPlayer')[0].src = this;
                          $('#audioPlayer')[0].play();
                          $('#songlist tr td').removeClass('current_song');
                          currentSong = $(this).parent().index();
                          $(this).parent().addClass('current_song');
                        });
                      }
            </script>
        </body>
    </html>""" % (header, page))
