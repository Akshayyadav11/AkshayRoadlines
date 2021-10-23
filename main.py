from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import uuid
from services.Users import users

app = Flask(__name__)

  
key  =  uuid.uuid4().hex  
app.secret_key = key


app.register_blueprint(users)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)