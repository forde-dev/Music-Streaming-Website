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
header = '''<header>
                <h1> Streaming </h1>
                <nav>
                  <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="streaming.py">Browse</a></li>
                    <li><a href="login.py">Login</a></li>
                    <li class="current"><a href="register.py">Register</a></li>
                  </ul>
                </nav>
            </header>'''
register = '''      <form action="register.py" method="post">
                        <fieldset>
                            <legend>Registration</legend>
                            <label for="username">Username: </label>
                            <input type="text" name="username" id="username" value="" />
                            <label for="email">Email: </label>
                            <input type="text" name="email" id="email" value="" />
                            <label for="password1">Password: </label>
                            <input type="password" name="password1" id="password1" />
                            <label for="passwords2">Re-enter password: </label>
                            <input type="password" name="password2" id="password2" />
                            <input type="submit" value="Register" />
                        </fieldset>
                    </form>'''
username = ''
email = ''
result = ''

if len(form_data) != 0:
    username = escape(form_data.getfirst('username', '').strip())
    email = escape(form_data.getfirst('email', '').strip())
    password1 = escape(form_data.getfirst('password1', '').strip())
    password2 = escape(form_data.getfirst('password2', '').strip())
    if not username or not email or not password1 or not password2:
        register = '''      <form action="register.py" method="post">
                                <fieldset>
                                    <legend>Registration</legend>
                                    <label for="username">Username: </label>
                                    <input type="text" name="username" id="username" value="%s" />
                                    <label for="email">Email: </label>
                                    <input type="text" name="email" id="email" value="%s" />
                                    <label for="password1">Password: </label>
                                    <input type="password" name="password1" id="password1" />
                                    <label for="passwords2">Re-enter password: </label>
                                    <input type="password" name="password2" id="password2" />
                                    <input type="submit" value="Register" />
                                </fieldset>
                            </form>''' % (username, email)
        result = '<p>Error: username, email and passwords are required</p>'
    elif password1 != password2:
        register = '''      <form action="register.py" method="post">
                                <fieldset>
                                    <legend>Registration</legend>
                                    <label for="username">Username: </label>
                                    <input type="text" name="username" id="username" value="%s" />
                                    <label for="email">Email: </label>
                                    <input type="text" name="email" id="email" value="%s" />
                                    <label for="password1">Password: </label>
                                    <input type="password" name="password1" id="password1" />
                                    <label for="passwords2">Re-enter password: </label>
                                    <input type="password" name="password2" id="password2" />
                                    <input type="submit" value="Register" />
                                </fieldset>
                            </form>''' % (username, email)
        result = '<p>Error: passwords must match</p>'
    else:
        try:
            connection = db.connect('localhost', 'root', 'fordemc2', 'projects')
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("""SELECT * FROM users 
                                  WHERE username = %s""", (username))
            if cursor.rowcount > 0:
                register = '''      <form action="register.py" method="post">
                                        <fieldset>
                                            <legend>Registration</legend>
                                            <label for="username">Username: </label>
                                            <input type="text" name="username" id="username" value="%s" />
                                            <label for="email">Email: </label>
                                            <input type="text" name="email" id="email" value="%s" />
                                            <label for="password1">Password: </label>
                                            <input type="password" name="password1" id="password1" />
                                            <label for="passwords2">Re-enter password: </label>
                                            <input type="password" name="password2" id="password2" />
                                            <input type="submit" value="Register" />
                                        </fieldset>
                                    </form>''' % (username, email)
                result = '<p>Error: user name already taken</p>'
            else:
                sha256_password = sha256(password1.encode()).hexdigest()
                cursor.execute("""INSERT INTO users (username, email, password) 
                                      VALUES (%s, %s, %s)""", (username, email, sha256_password))
                connection.commit()
                cursor.close()
                connection.close()
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
                            </header>''' % (username)
                register = ''
                result = """
                       <p>Succesfully Registered!</p>
                       <p>Still in Development, Come back soon</p>
                       <ul>
                           <li><a href="protected_library.py">Your Library</a></li> 
                           <li><a href="logout.py">Logout</a></li>
                       </ul>"""
                print(cookie)
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
        </html>""" % (header, register, result))
