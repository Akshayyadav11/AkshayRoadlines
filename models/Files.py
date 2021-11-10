from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, send_file,jsonify
from flask_mysqldb import MySQL
from models.BaseDB  import BaseDB  
import re
import tempfile
import os
import io
import pandas as pds
import matplotlib.pyplot as plt
import sys
import numpy as np

class Files(BaseDB):    
    def __init__(self):
        self.db = BaseDB()
      
    
    def fileupload(self,file, filedata):
        try:
            
            connection = self.db.get_connection()
            cursor = connection.cursor(dictionary=True)
            print("file---session",session)
            # userid = session['id']
            # username = session['username']
            userid= session['profile']['userId']
            username = session['profile']['emailId']
            
            filename,filetype = os.path.splitext(file)
            print("---filename----",userid, username, filename,filetype)
            cursor.execute('INSERT INTO documents VALUES (NULL,%s, %s, %s, %s,%s, %s, %s, %s)', (userid, filename, filedata,filetype,datetime.now() ,username,'00:00:00', '', ))
            connection.commit()
            msg = 'File uploaded successfully !'
            print("msg--",msg)
           
            return msg
        except Exception as e:
            print(e)
            raise e
    
    def filedownload(self,docid):
        try:
            
            connection = self.db.get_connection()
            cursor = connection.cursor(dictionary=True)
            query = 'SELECT * FROM documents WHERE documentid = %s'
            cursor.execute(query,(docid, ))
            result = cursor.fetchone()
            
            byte_data = result["filedata"]
            filename = result["filename"]
            
            data__res = send_file(io.BytesIO(byte_data),
                                                mimetype='multipart/form-data',
                                                as_attachment=True,
                                                attachment_filename=filename)
            data__res.headers["filename"] = filename
            data__res.headers[
                "Access-Control-Expose-Headers"] = 'filename'
            return data__res
            
        except Exception as e:
            print(e)
            raise e
    

    def read_excel_file(self,excel_file):
        try:
            
            connection = self.db.get_connection()
            cursor = connection.cursor(dictionary=True)
           
            dataframe = pds.read_excel(excel_file)
            
            # xpoints = np.array([1, 8])
            # ypoints = np.array([3, 10])

            # plt.plot(xpoints, ypoints)
            # plt.show()
            # plt.savefig(sys.stdout.buffer)
            return dataframe
            
        except Exception as e:
            print(e)
            return jsonify({"error":'Error while reading excel file'},500)