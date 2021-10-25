from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL
from models.BaseDB  import BaseDB  
import re
import tempfile

class Files(BaseDB):    
    def __init__(self):
        self.db = BaseDB()
      
    
    def convertToBinaryData(self,filename):
        # Convert digital data to binary format
        # f = tempfile.TemporaryFile()
        with open(filename, 'r') as file:
           binaryData = file.read()
        return binaryData

    def fileupload(self,req_file):
        try:
            filename = req_file.filename;
            print("--req_file-filename----",req_file.filename)
            req_file.save(req_file.filename)
            filedata  = self.convertToBinaryData(req_file.filename)
           
            print("---filename----", filename)
            connection = self.db.get_connection()
            cursor = connection.cursor(dictionary=True)

            userid = session['id']
            username = session['username']
            print("---filename----",userid, username, filename)
            cursor.execute('INSERT INTO documents VALUES (NULL,%s, %s, %s,%s, %s, %s, %s)', (userid, filename, filedata,datetime.now() ,username,'00:00:00', '', ))
            connection.commit()
            msg = 'File uploaded successfully !'
            print("msg--",msg)
           
            return msg
        except Exception as e:
            print(e)
            raise e
        