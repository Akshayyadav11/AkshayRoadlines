
from flask import Flask, render_template,request, redirect, url_for, make_response,session, jsonify,Blueprint, flash
from flask_mysqldb import MySQL
from models.BaseDB  import BaseDB  
import re


from models.Files import Files

files = Blueprint("files", __name__)



@files.route('/upload')
def upload():
   return render_template('fileupload.html')
	

@files.route('/uploader', methods =['POST'])
def uploader():
    try:
        
        if request.method == 'POST' and request.files['file'].filename:
            
            req_file = request.files['file'].filename
            bytedata = request.files['file'].read()
            
            filemodel = Files()
            response_data  = filemodel.fileupload(req_file,bytedata)
            print("--response_data-",response_data)
        else:
            response_data  = "File not selected"           
            print("--response_data-",response_data)
        return render_template('fileupload.html', msg  = response_data )

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
        


@files.route('/downloader', methods =['POST'])
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