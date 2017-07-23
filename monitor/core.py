#!/usr/bin/env python
# -*- coding: utf-8 -*-

# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
             render_template, flash

# configuration
#DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = '123123'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

#file_path = os.path.dirname(os.path.abspath(__file__))
#print file_path

@app.route('/')
def main():
    return render_template(r'monitor/templates/main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('main'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('main'))

def run():
    app.run()

if __name__ == '__main__':
    # app.run()
    pass
