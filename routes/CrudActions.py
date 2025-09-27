from datetime import datetime
import time
import re
from flask import request, render_template, url_for
from passlib.handlers.sha2_crypt import sha256_crypt
from sqlalchemy import Integer
from sqlalchemy.sql.functions import now
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash

from src.DBConnect import *
from flask_login import login_required, current_user
from src.models.Admin import *
from src.routes.Login import requires_roles

Status =''

@app.route('/allusers')
@login_required
@requires_roles('Admin')
def UserModule():
    User_List = db.session.query(Users.id,Users.Role_ID,Users.User_Status,
                                 Users.Date_Created,Users.EmailAddress,
                                 Users.Other_Names,Users.Sur_Name,Users.UserName,
                                 Roles.Role_type,User_Status.Status_type, Gender.Gender)\
        .join(Roles, Roles.Role_ID == Users.Role_ID)\
        .join(User_Status,User_Status.Status_ID == Users.User_Status)\
        .join(Gender, Gender.ID==Users.GenderID)\
        .filter(Users.UserName.ilike('%' + '' + '%'))
    Roles_List = Roles.query.all()
    return render_template('Admin/users.html', User_List=User_List,Roles_List=Roles_List)

@app.route('/users', methods=['GET','POST'])
@login_required
@requires_roles('Admin')
def ReassignRole():
    if request.method=='POST':
        UserID = str(re.sub('[^0-9]+', '',request.form['UserID']))
        RolesAssigned = str(re.sub('[^0-9]+', '',request.form['Role']))
        UpdateUserRole = Users.query.filter_by(id=UserID).first()
        UpdateUserRole.Role_ID=RolesAssigned
        db.session.commit()
    flash("User Role Updated successfully")
    return redirect(url_for('UserModule'))

@app.route('/resetpass', methods=['GET','POST'])
@login_required
@requires_roles('Admin')
def ResetPass():
    if request.method=='POST':
        UserID = str(re.sub('[^0-9z]+', '',request.form['UserID']))
        ResetUserPass = Users.query.filter_by(id=UserID).first()
        ResetUserPass.Pass_word = sha256_crypt.encrypt("password")
        db.session.commit()
    flash("Password Reset successfully")
    return redirect(url_for('UserModule'))


@app.route('/UpdateMyProfile', methods=['GET','POST'])
@login_required
def UpdateMyProfile():
    if request.method=='POST':
        SurName = str(re.sub('[^A-Za-z]+', '',request.form['surName']))
        OtherNames = str(re.sub('[^A-Za-z]+ ', '',request.form['otherNames']))
        Gender = str(re.sub('[^0-9]+', '',request.form['Gender']))
        Nationality = str(re.sub('[^A-Za-z]+', '',request.form['Nationality']))
        DoB = str(re.sub('[^0-9 /]+', '',request.form['DoB']))
        UserEdited = Users.query.filter_by(id=current_user.id).first()
        UserEdited.Sur_Name = SurName
        UserEdited.Other_Names = OtherNames
        UserEdited.Nationality = Nationality
        UserEdited.GenderID = Gender
        UserEdited.DoB = DoB
        db.session.commit()
        flash("Profile Updated Successfully")
    return redirect(url_for('EditProfile'))

@app.route('/changePassword', methods=['GET','POST'])
@login_required
def ChangePassword():
    if request.method=='POST':
        CurrentPassword =str(request.form['currentPassword']).strip()
        NewPassword = str(request.form['newPassword']).strip()
        CurrentUser = Users.query.filter(Users.id== current_user.id).first()
        if sha256_crypt.verify(CurrentPassword, CurrentUser.Pass_word):
            try:
                CurrentUser.Pass_word = sha256_crypt.encrypt(NewPassword)
                db.session.commit()
                db.session.close()
                flash("Password Changed Successfully")
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
        else:
            flash("Wrong Password. Please provide the correct password")
    return redirect(url_for('EditProfile'))

@login_required
@requires_roles('Admin')
def LoadUserData():
    All_Users = Users.query.all()
    return All_Users


#ts = time.time()
 #       st = datetime.fromtimestamp(ts).strftime('%y-%m-%d %H:%M:%S')
