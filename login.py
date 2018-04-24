#!/usr/bin/env python


from cgitb import enable
enable()

from cgi import FieldStorage
from html import escape
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie
import pymysql as db

form_data = FieldStorage()
header = '''
            <header>
                <h1> Streaming </h1>
                <nav>
                  <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="streaming.py">Browse</a></li>
                    <li class="current"><a href="login.py">Login</a></li>
                    <li><a href="register.py">Register</a></li>
                  </ul>
                </nav>
            </header>'''
login = '''
                <form action="login.py" method="post">
                    <fieldset>
                        <legend>Login</legend>
                        <label for="username">User name: </label>
                        <input type="text" name="username" id="username" value="" />
                        <label for="password">Password: </label>
                        <input type="password" name="password" id="password" />
                        <input type="submit" value="Login" />
                    </fieldset>
                </form>'''

username = ''
result = ''


if len(form_data) != 0:
    username = escape(form_data.getfirst('username', '').strip())
    password = escape(form_data.getfirst('password', '').strip())
    if not username or not password:
        login = '''
                <form action="login.py" method="post">
                    <fieldset>
                        <legend>Login</legend>
                        <label for="username">User name: </label>
                        <input type="text" name="username" id="username" value="%s" />
                        <label for="password">Password: </label>
                        <input type="password" name="password" id="password" />
                        <input type="submit" value="Login" />
                    </fieldset>
                </form>''' % (username)
        result = '<p>Error: user name and password are required</p>'
    else:
        sha256_password = sha256(password.encode()).hexdigest()
        try:
            connection = db.connect('localhost', 'root', 'fordemc2', 'projects')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM users 
                              WHERE username = %s
                              AND password = %s""", (username, sha256_password))
            if cursor.rowcount == 0:
                login = '''
                        <form action="login.py" method="post">
                            <fieldset>
                                <legend>Login</legend>
                                <label for="username">User name: </label>
                                <input type="text" name="username" id="username" value="%s" />
                                <label for="password">Password: </label>
                                <input type="password" name="password" id="password" />
                                <input type="submit" value="Login" />
                            </fieldset>    
                        </form>''' % (username)
                result = '<p>Error: incorrect username or password</p>'
            else:
                cookie = SimpleCookie()
                sid = sha256(repr(time()).encode()).hexdigest()
                cookie['sid'] = sid
                session_store = open('sess_' + sid, writeback=True)
                session_store['authenticated'] = True
                session_store['username'] = username
                session_store.close()
                header = '''
                            <header>
                                <h1> Streaming </h1>
                                <nav>
                                  <ul>
                                    <li><a href="protected_streaming.py">Browse</a></li>
                                    <li><a href="protected_library.py">Library</a></li>
                                    <li class="current"><a href="profile.py">%s</a></li>
                                    <li><a href="logout.py">Logout</a></li>
                                  </ul>
                                </nav>
                            </header>''' % username
                login = ''
                result = """
                    <p>Succesfully logged in! Welcome back %s</p>
                    <p>Do you want to view <a href="protected_library.py">Your Library</a>? 
                    <p><a href="logout.py">Logout</a></p>
                    """ % username
                print(cookie)
            cursor.close()
            connection.close()
        except (db.Error, IOError):
            result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print('Content-Type: text/html')
print()
print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta name="viewport" content="width=device-width"/>
            <meta charset="utf-8" />
            <title>Streaming</title>
            <link rel="stylesheet" href="styles.css" />
        </head>
        <body>
            %s
            <main>
                %s
                %s
            </main>
        </body>
    </html>""" % (header, login, result))