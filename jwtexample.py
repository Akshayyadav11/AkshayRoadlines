from flask.helpers import make_response
import jwt
from flask import Flask, request, jsonify
import datetime

import json
from functools import wraps

app1 = Flask(__name__)

app1.config['SECRET_KEY']  =  "secretekey"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message':"Token is missing"}), 403        
        try:
            data = jwt.decode(token,app1.config['SECRET_KEY'] )
        except:
            return jsonify({'message':"Token is invalid"}),403
        return f(*args, **kwargs)
    return decorated



app1.route('/')
app1.route('/loggin', methods=['POST','GET'])
def loggin():
    auth= request.authorization
    if auth:
        token = jwt.encode({'user':auth.username,"expr":datetime.datetime.utcnow() + datetime.timedelta(minutes=30)})

        return jsonify({'message':token}) 



app1.route('/restricted')
@token_required
def secure():
    return jsonify({"message":"availble for valid users"})

app1.route('/unrestricted')
def unrestricted():
    return jsonify({"message":"availble for limited users"})

if __name__ == '__main__':
    app1.run('127.0.0.1','6000',debug=True)
    
