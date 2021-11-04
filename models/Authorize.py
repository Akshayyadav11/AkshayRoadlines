
from flask import current_app as app
import datetime 
from datetime import timedelta
from functools import wraps
from flask import Flask, config,make_response,jsonify, request, redirect
from flask.globals import session
import jwt

class Authorize():
    # def token_required(func):
    #     @wraps(func)
    #     def decorated(*args, **kwrags):
    #         try:
    #             token=""
    #             # if 'Authorization' in request.headers:
    #             #     data = request.headers['Authorization']
    #             #     token = str.replace(str(data), 'Bearer ', '')
    #             print("--authorize-session-",session['profile'])
    #             if 'profile' not in session:
    #                 print('profile not in session')
    #                 return redirect('/login')
    #             # token = request.args.get('token')
    #             # token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NywiZXhwIjoxNjM1NzUwMjk0fQ.UbVtIq3ftwFgj4qig22kE9CFH0KhqG2f2A7ygnUxxhE"
    #                 # print("---------token-",token)
    #             # if not token:
    #             #     return jsonify({"message":'Token is missing'},500)
    #             try:
    #                 payload = jwt.decode(session['profile']['access_token'], app.config['SECRET_KEY'],algorithms=["HS256"])
    #                 print("payload-----",payload)
    #             except:
    #                 return jsonify({"Invalid token"})
    #         except Exception as exc:
    #             print('------profile---exception',exc)
    #             return jsonify({"message":'Token is Expired/Invalid'},500)
    #             # raise (str(exc))
    #         # return payload 
            
    #         return func(*args, **kwrags)
    #     return decorated

    def token_required(func):
        @wraps(func)
        def decorated(*args, **kwrags):
            try:
                token=""
                if 'Authorization' in request.headers:
                    data = request.headers['Authorization']
                    token = str.replace(str(data), 'Bearer ', '')
                    print("token---",token)
                if not token:
                    return make_response(
                        'Token is missing !!',
                        401,
                        {'WWW-Authenticate' : 'Basic realm ="Login Required !!"'}
                    ) 
                try:
                    payload = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
                    print("payload-----",payload)
                except:
                    return jsonify({"Invalid token"})
            except Exception as exc:
                
                return make_response(
                        'The access token expired/Invalid !!',
                        401,
                        {'WWW-Authenticate' : 'Basic realm ="Login Required !!"'}
                    ) 
                    
                # return jsonify({"message":'Token is Expired/Invalid'},500)
                # raise (str(exc))

            
            
            return func(*args, **kwrags)
        return decorated

    def create_access_token(response_data):
        access_token = jwt.encode({'userId':response_data['id'],'emailId':response_data['email'], 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        return access_token
    
    def create_refresh_token(response_data):
        refresh_token = jwt.encode({'userId':response_data['id'],'emailId':response_data['email'], 'grant_type':'refresh'},app.config['SECRET_KEY'])
        return refresh_token