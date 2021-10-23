from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL
from models.BaseDB  import BaseDB  
import re

class Users(BaseDB):    
    def __init__(self):
        self.db = BaseDB()
        print("----",self.db)
    
    def login(self, username, password):
        try:
            msg = ''
            connection = self.db.get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password, ))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                print(session)     
                msg ='Logged in successfully !'  
            else:             
                msg ='Incorrect username / password !'

            return msg
        except Exception as e:
            print(e)

    
    def register(self, email, username, password):
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username, ))
            account = cursor.fetchone()
            print("---------",account)
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers !'
            elif not username or not password or not email:
                msg = 'Please fill out the form !'
            
            else:
                cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email, ))
                connection.commit()
                msg = 'You have successfully registered !'
            print("msg--",msg)
            
            return msg
        except Exception as e:
            print(e)