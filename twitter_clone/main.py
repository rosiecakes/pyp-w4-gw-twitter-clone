import time
import sqlite3
from hashlib import md5
from functools import wraps
from flask import Flask
from flask import (g, request, session, redirect, render_template,
                   flash, url_for)

app = Flask(__name__)


def connect_db(db_name):
    return sqlite3.connect(db_name)


@app.before_request
def before_request():
    g.db = connect_db(app.config['DATABASE'][1])
    g.user = None
    if 'username' in session: 
        g.user = session['username']


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    if g.user:
        # username = g.user
        # return redirect(url_for('feed', username=g.user))
        return g.user
        
    return redirect(url_for('login'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        
        if password == 'password':
            session['username'] = username
            return redirect(url_for('feed', username=username))
        flash('Incorrect username or password')
        # mdpass = md5(password.encode('utf-8')).hexdigest()
        
        #cursor = g.db.execute("SELECT id FROM user WHERE username=? AND password=?", (username, mdpass))
        # all_users = g.db.execute('SELECT id, username, password FROM user')
        # for user in all_users:
        #     if username == user[1] and password == user[2]:
        #         return redirect(url_for('profile'))
        #     else:
        #         flash('Incorrect username or password')
        #         return render_template('login.html')
                
    return render_template('login.html')
        
    
@app.route('/<username>')
def feed(username):
    # cursor = g.db.execute('SELECT username, created, content FROM user, tweet WHERE user.id = tweet.user_id;')
    # tweet = [dict(username=row[0], created=row[1], content=row[2]) for row in cursor.fetchall()]
    # if session['username']:
    #     return ('i am feed for {}').format(username)
    return ('no user')

# @app.route('/profile', methods = ['POST', 'GET'])
# def profile():
#     if request.method == 'GET':
#         return ('user profile')
#     return ('type is post')
    # if request.method == 'POST':
    #     username = request.form['username']
    #     first_name = request.form['first_name']
    #     last_name = request.form['last_name']
    #     birth_date = request.form['birth_date']
       
    #     g.db.execute("UPDATE user SET first_name=?, last_name=?, birth_date=? WHERE username=?", (first_name, last_name, birth_date, username))
    #     g.db.commit()
    #     flash('Profile has been updated')
            
    # cursor = g.db.execute("SELECT username, first_name, last_name, birth_date FROM user WHERE username=?", (username))
    # # no this will not work ^ we are not being passed username, we need to get the id from the session instead
    # profile_info = [dict(username=row[0], first_name=row[1], last_name=row[2], birth_date=row[3]) for row in cursor.fetchall()]
         
    # return render_template('profile.html', profile_info=profile_info)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# @app.route('/tweets/(the tweet id)/delete')
# def delete():
#     pass