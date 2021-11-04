from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, send_file
from flask_mysqldb import MySQL
from models.BaseDB  import BaseDB  
import re
import tempfile
import os
import io

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
    