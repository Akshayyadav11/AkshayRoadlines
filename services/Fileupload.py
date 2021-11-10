
from flask import Flask, render_template,request, redirect, url_for, make_response,session, jsonify,Blueprint, flash
from flask_mysqldb import MySQL
from models.Authorize import Authorize
from models.BaseDB  import BaseDB  
import re


from models.Files import Files

files = Blueprint("files", __name__)


@files.route('/index')
@Authorize.token_required
def index():
   return render_template('index.html')
	

@files.route('/upload')
def upload():
   return render_template('fileupload.html')
	

@files.route('/uploader', methods =['POST'])
@Authorize.token_required
def uploader():
    try:
        
        if request.method == 'POST' and request.files['file'].filename:
            
            req_file = request.files['file'].filename
            bytedata = request.files['file'].read()
            
            filemodel = Files()
            response_data  = filemodel.fileupload(req_file,bytedata)
            print("--response_data-",response_data)
            return jsonify({"message": str(response_data)}), 200
        else:
            response_data  = "File not selected"           
            print("--response_data-",response_data)
        # return render_template('fileupload.html', msg  = response_data )
            return jsonify({"message": str(response_data)}), 500

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
        


@files.route('/downloader', methods =['POST'])
@Authorize.token_required
def downloader():
    try:
        
        if request.method == 'POST':
            
            
            request_data = request.get_json()
            docuid  = request_data.get('docid')
            
            filemodel = Files()
            response_data  = filemodel.filedownload(docuid)
            print("-succ-response_data-",response_data)
        else:
            response_data  = "File not able to download"           
            print("--response_data-",response_data)

        return response_data

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500   
    

    
@files.route('/readexcel', methods =['POST'])
@Authorize.token_required
def read_excel():
    try:
        
        if request.method == 'POST' and request.files['file'].filename:
            
            excel_file = request.files['file']
            req_file = request.files['file'].filename
            bytedata = request.files['file'].read()
            
            filemodel = Files()
            response_data  = filemodel.read_excel_file(excel_file)
            print("--response_data-",response_data)
            return jsonify({"message": str(response_data)}), 200
        else:
            response_data  = "File not selected"           
            print("--response_data-",response_data)
        # return render_template('fileupload.html', msg  = response_data )
            return jsonify({"message": str(response_data)}), 500

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500