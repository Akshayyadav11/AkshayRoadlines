
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

 
@users.route('/register', methods =['POST','GET'])
def register():
    try:
        print(request.method)
        msg = ''
        username = ''
        password = ''
        email = ''
        if (request.method == 'POST' or request.method == 'POST' ) and 'username' in request.form and 'password' in request.form and 'email' in request.form :
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            print("---",username,password,email)
            registerDetails =  Users()
            response_data = registerDetails.register(email, username, password)
            print("response_data--",response_data)
            if response_data  == "You have successfully registered !":
                print("response_data--",response_data)
                return render_template('login.html', msg = response_data)

            else:
                return render_template('register.html', msg = response_data)
        
        
        elif request.method == 'GET' or request.method == 'POST':
            return render_template('register.html',msg  = "please fill out all details")

    except Exception as e: 
        print(e)       
        return jsonify({"error": str(e)}), 500
      

@users.route('/logout')
def logout():
    print("-----befo----",session)
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    print("---afte------",session)
    return redirect(url_for('users.login'))

# @users.route('/')
# @users.route('/login', methods =['GET', 'POST'])
# def login():
#     try:       
#         msg = ''
#         if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#             username = request.form['username']
#             password = request.form['password']
#             loginDetails =  Users()
#             response_data = loginDetails.login(username, password)
#             if response_data =="Logged in successfully !":
#                 print("response_data--",response_data)
#                 return render_template('index.html', msg = response_data)
#             else:
#                 return render_template('login.html', msg = response_data)
#         else:
            
#             return redirect(url_for('users.login', msg  = "login failed")) 
#     except Exception as e:
#         print(e)
#         raise e
        
# @users.route('/logout')
# def logout(self):
#     session.pop('loggedin', None)
#     session.pop('id', None)
#     session.pop('username', None)
#     return redirect(url_for('login'))         
    
    
# @users.route('/register', methods =['GET', 'POST'])
# def register(self):
#     msg = ''
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         connection = self.db.get_connection()
#         cursor = connection.cursor(dictionary=True)

#         cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
#         account = cursor.fetchone()
#         if account:
#             msg = 'Account already exists !'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             msg = 'Invalid email address !'
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             msg = 'Username must contain only characters and numbers !'
#         elif not username or not password or not email:
#             msg = 'Please fill out the form !'
#         else:
#             cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
#             connection.commit()
#             msg = 'You have successfully registered !'
#     elif request.method == 'POST':
#         msg = 'Please fill out the form !'
#     return render_template('register.html', msg = msg)
    