
from flask import Flask, render_template,request, redirect, url_for, make_response,session, jsonify,Blueprint, flash
from flask_mysqldb import MySQL
from models.BaseDB  import BaseDB  
import re


from models.Users import Users

users = Blueprint("users", __name__)


@users.route('/')
@users.route('/login', methods =['GET', 'POST'])
def login():
    try:     
        msg = '' 
        response_data = ''           
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    
            username = request.form['username']
            password = request.form['password']
            print("---",username,password)
            loginDetails =  Users()
            response_data = loginDetails.login(username, password)
            if response_data  == "Logged in successfully !":
                print("response_data--",response_data)
                return render_template('index.html', msg = response_data)
               
            else:
                return render_template('login.html', msg = response_data)
               
        else:
            
            return render_template('login.html')
        
    except Exception as e: 
        print(e)       
        return jsonify({"error": str(e)}), 500   

