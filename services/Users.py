
from flask import Flask, render_template,request, redirect, url_for, make_response,session, jsonify,Blueprint, flash
from flask_mysqldb import MySQL
from models.BaseDB  import BaseDB  
import re
from datetime import datetime, timedelta
from functools import wraps
import jwt
from  werkzeug.security import generate_password_hash, check_password_hash

from models.Users import Users

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
            response_data = loginDetails.login(emailId, password)
            if response_data  == "Logged in successfully !":
                return render_template('index.html', msg = response_data)
            else:
                return render_template('login.html', msg = response_data)
               
        else:
            
            return render_template('login.html')
        
    except Exception as e: 
        print(e)       
        return jsonify({"error": str(e)}), 500   

