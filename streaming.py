#!/usr/bin/env python


from cgitb import enable
enable()
from html import escape
from cgi import FieldStorage

import pymysql as db


print("Content-type: text/html")
print()

result = ''
search = ''
genre = ''
sort = ''
sql = ''
form_data = FieldStorage()


try:
    connection = db.connect('localhost', 'root', 'fordemc2', 'projects')
    cursor = connection.cursor(db.cursors.DictCursor)
    cursor.execute("""SELECT * FROM music""")
    result = """<table id='songlist'>
                <tr><th colspan="3">All Music</th></tr>
                <tr><th>Name</th><th>Artist</th></tr>"""

    for row in cursor.fetchall():
        result += """<tr>
                        <td><a href='%s'>%s</a></td>
                        <td>%s</td>
                     </tr>""" % (row['location'], row['name'], row['artist'])
    result += '</table>'
    cursor.close()

    if len(form_data) != 0:

        search = escape(form_data.getfirst('search', '')).strip()
        genre = escape(form_data.getfirst('genre','')).strip()
        sort = escape(form_data.getfirst('sort','')).strip()

        genre_selection = ['rock', 'punk', 'hiphop', 'electric', 'freaky', '']
        sort_selection = ['song_id', 'artist', 'name', 'date_of_release']

        cursor = connection.cursor(db.cursors.DictCursor)
        if genre in genre_selection and sort in sort_selection and search == '':
            if genre == "":
                cursor.execute("""SELECT * FROM music ORDER BY %s""" % (sort))
            elif sort == "song_id":
                cursor.execute("""SELECT * FROM music WHERE genre = %s""", (genre))
            else:
                cursor.execute("""SELECT * FROM music WHERE genre = '%s' ORDER BY %s""" % (genre, sort))

        if search != '':
            cursor.execute("""SELECT * FROM music where name = %s or artist = %s""", (search, search))

        result = """<table id='songlist'>
                        <tr><th colspan="3">All Music</th></tr>
                        <tr><th>Name</th><th>Artist</th></tr>"""

        for row in cursor.fetchall():
            result += """<tr>
                                <td><a href='%s'>%s</a></td>
                                <td>%s</td>
                             </tr>""" % (row['location'], row['name'], row['artist'])
        result += '</table>'
        cursor.close()
    connection.close()

except db.Error:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'


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
            <header>
                <h1> Streaming </h1>
                <nav>
                  <ul>
                    <li><a href="index.html">Home</a></li>
                    <li class="current"><a href="streaming.py">Browse</a></li>
                    <li><a href="login.py">Login</a></li>
                    <li><a href="register.py">Register</a></li>
                  </ul>
                </nav>
            </header>
            <main>
                <form action='streaming.py' method='get'>
                    <label for="search">Search: </label>
                    <input type="text" name="search" value="%s">
                    <label for="sort">Sort By: </label>
                    <select name="sort">
                        <option value="song_id">All</option>
                        <option value="artist">Artist</option>
                        <option value="name">Song Name</option>
                        <option value="date_of_release">Release Date</option>
                    </select>
                    <label for="genre">Pick a Genre: </label>
                    <select name="genre">
                        <option value="">All</option>
                        <option value="rock">Rock</option>
                        <option value="hiphop">HipHop</option>
                        <option value="punk">Punk</option>
                        <option value="electric">Electric</option>
                        <option value="freaky">Freaky</option>
                    </select>
                    <input type="submit" />
                </form>
                <audio controls source src='' type='audio/mp3' id='audioPlayer'>
                    <p>Sorry, Your browser doesn't support HTML5</p>
                </audio>
                %s
            </main>
            <aside>
            </aside>
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
    </html>""" % (search, result))
