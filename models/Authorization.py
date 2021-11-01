
from flask import current_app as app
import datetime 
from datetime import timedelta
from functools import wraps
from flask import Flask, config,make_response,jsonify, request
import jwt

class Authorization():
    def token_required(func):
        @wraps(func)
        def decorated(*args, **kwrags):
            token=""
            if 'Authorization' in request.headers:
                data = request.headers['Authorization']
                token = str.replace(str(data), 'Bearer ', '')
            # token = request.args.get('token')
            # token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NywiZXhwIjoxNjM1NzUwMjk0fQ.UbVtIq3ftwFgj4qig22kE9CFH0KhqG2f2A7ygnUxxhE"
                print("---------token-",token)
            if not token:
                return jsonify({"message":'Token is missing'},500)
            try:
                payload = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
                print("payload-----",payload)
            # except:
            #     return jsonify({"Invalid token"})
            except (jwt.InvalidTokenError, jwt.ExpiredSignature, jwt.DecodeError) as exc:
                raise (str(exc))
            # return payload 
            
            return func(*args, **kwrags)
        return decorated