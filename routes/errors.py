from flask import render_template, url_for, request
from passlib.handlers.sha2_crypt import sha256_crypt
from werkzeug.utils import redirect
from werkzeug.exceptions import InternalServerError, BadRequest
from datetime import datetime

from src.models.Admin import *
from src.DBConnect import app, db

# Internal Error Page
@app.errorhandler(InternalServerError)
def ServerError(e):
    # note that we set the 404 status explicitly
    ErrorMsg ="NOPE!!!! " + str(e)
    return render_template('404.html',ErrorMsg=ErrorMsg)

@app.errorhandler(InternalServerError)
def handle_500(e):
    ErrorMsg ="NOPE!!!! " + str(e)
    print(e)
    return render_template('404.html',ErrorMsg=ErrorMsg)


# forbiden Pages
@app.errorhandler(413)
def filetoolarge(e):
    # note that we set the 404 status explicitly
    ErrorMsg = "NOPE!!!! "   + str(e)
    #return render_template('404.html', ErrorMsg=ErrorMsg)
    return redirect(url_for('UserLogin'))

@app.errorhandler(405)
def notallowed(e):
    # note that we set the 404 status explicitly
    return redirect(url_for('UserLogin'))

@app.errorhandler(404)
def unauthorized(e):
    # note that we set the 404 status explicitly
    return redirect(url_for('UserLogin'))

@app.errorhandler(403)
def forbidden(e):
    # note that we set the 404 status explicitly
    ErrorMsg = "NOPE!!!! Forbidden"
    return redirect(url_for('UserLogin'))

@app.errorhandler(401)
def unauthorized(e):
    # note that we set the 404 status explicitly
    return redirect(url_for('UserLogin'))

@app.errorhandler(400)
def BadRequest(e):
    # note that we set the 404 status explicitly
    ErrorMsg = "NOPE!!!! " + str(e)
    return redirect(url_for('UserLogin'))