from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL
from models.BaseDB  import BaseDB  
import re

class Users(BaseDB):    
    def __init__(self):
        self.db = BaseDB()
        print("----",self.db)
    
    def login(self, emailId):
        try:
            msg = ''
            connection = self.db.get_connection()
            cursor = connection.cursor(dictionary=True)

            # cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (emailId, password, ))
            cursor.execute('SELECT * FROM accounts WHERE email = %s ', (emailId, ))
           
            account = cursor.fetchone()
            # if account:
            #     session['loggedin'] = True
            #     session['id'] = account['id']
            #     session['emailId'] = account['email']
            #     print(session)     
            #     msg ='Logged in successfully !'  
            # else:             
            #     msg ='Incorrect emailId / password !'

            # return msg
            # print("---session-",session)
            return account
        except Exception as e:
            print(e)

    