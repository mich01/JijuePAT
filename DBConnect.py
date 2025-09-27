from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
from datetime import timedelta




# connection code
from flask_sqlalchemy import SQLAlchemy

app: Flask = Flask(__name__)

#the sqlalchemy is set to track y default this command disallows that feature
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
#app.config['MYSQL_HOST'] ='localhost'
#app.config['MYSQL_USER'] ='root'
#app.config['MYSQL_PASSWORD'] =''
#app.config['MYSQL_DB'] ='jijue_db'
#app.config['MYSQL_CURSORCLASS'] ='DictCursor'
#connection databse
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:@localhost:3306/jijue_db'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(hours=6)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#instatiate the db model
db=SQLAlchemy(app)