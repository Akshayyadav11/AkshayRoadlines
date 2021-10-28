
from flask import Flask, render_template,request, redirect, url_for, make_response,session, jsonify,Blueprint, flash
from flask_mysqldb import MySQL
from models.BaseDB  import BaseDB  
import re


from models.Register import Register

users = Blueprint("users", __name__)
registers = Blueprint("registers", __name__)

@registers.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    response_data = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'emailId' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['emailId']
        registerDetails =  Register()
        print("--registerDetails",registerDetails)
        response_data = registerDetails.register(email, username, password)
    elif request.method == 'POST':
        response_data = 'Please fill out the form !'
    return render_template('register.html', msg = response_data)

@registers.route('/logout')
def logout():
    print("-----befo----",session)
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('emailId', None)
    print("---afte------",session)
    return redirect(url_for('users.login'))