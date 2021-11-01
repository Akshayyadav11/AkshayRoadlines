
from flask import Flask, render_template,request, redirect, url_for, make_response,session, jsonify,Blueprint, flash
from flask_mysqldb import MySQL
from models.BaseDB  import BaseDB  
import re
import datetime
from datetime import timedelta
from functools import wraps
import jwt
from  werkzeug.security import generate_password_hash, check_password_hash

from models.Users import Users
from flask import current_app as app

users = Blueprint("users", __name__)

@users.route('/')
@users.route('/login', methods =['GET', 'POST'])
def login():
    try:     
        msg = '' 
        response_data = ''           
        if request.method == 'POST' and 'emailId' in request.form and 'password' in request.form:
    
            emailId = request.form['emailId']
            password = request.form['password']
            print("---",emailId,password)
            loginDetails =  Users()
            response_data = loginDetails.login(emailId)
            if response_data is None:
                return make_response(
                        'Could not verify login',
                        401,
                        {'WWW-Authenticate' : 'Basic realm ="Login Required !!"'}
                    ) 
            
            if check_password_hash(response_data['password'],password):
                print("-------in inf-------")
                token = jwt.encode({'id':response_data['id'], 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
                print("token---", token)

                return make_response(jsonify({'token' : token}), 201)
            
            print("check_password_hash--else-")
            return make_response(
                    'Could not verify hash',
                    401,
                    {'WWW-Authenticate' : 'Basic realm ="Login Required !!"'}
                ) 

        #     if response_data  == "Logged in successfully !":
        #         return render_template('index.html', msg = response_data)
        #     else:
        #         return render_template('login.html', msg = response_data)
               
        else:
            
            return render_template('login.html')
        
    except Exception as e: 
        print(e)       
        return jsonify({"error": str(e)}), 500   

