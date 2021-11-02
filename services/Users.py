
from flask import Flask, render_template,request, redirect, url_for, make_response,session, jsonify,Blueprint, flash
from flask_mysqldb import MySQL
from werkzeug.datastructures import Authorization
from models.Authorize import Authorize
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
                        'Could not verify!!',
                        401,
                        {'WWW-Authenticate' : 'Basic realm ="Login Required !!"'}
                    ) 
            
            if check_password_hash(response_data['password'],password):
                print("-------in inf-------")
                access_token = jwt.encode({'userId':response_data['id'],'emailId':response_data['email'], 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
                # print("token---", access_token)

                refresh_token = jwt.encode({'userId':response_data['id'],'emailId':response_data['email'], 'grant_type':'refresh', 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
               
                return make_response(jsonify({
                                    'access_token' : access_token,
                                    'refresh_token':refresh_token,
                                    'userId':response_data['id'],
                                    'emailId':response_data['email'],
                                    'message':'Logged in successfully'
                                    }), 201)
            
            print("check_password_hash--else-")
            return make_response(
                    'Could not verify passoword !!',
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



@users.route('/protected', methods =['GET', 'POST'])
@Authorize.token_required
def protected():
    return jsonify({"message": str("protected")}), 200 


@users.route('/unprotected', methods =['GET', 'POST'])
def unprotected():
    return jsonify({"message": str("unprotected")}), 200 