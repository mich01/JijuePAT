from datetime import datetime
from flask import request, render_template, url_for, session
from flask_security import UserMixin, RoleMixin
from passlib.handlers.sha2_crypt import sha256_crypt
from sqlalchemy import or_
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from functools import wraps
from src.DBConnect import *
from flask_login import LoginManager, login_required,current_user,  login_user, logout_user
from src.models.Admin import *
from src.models.Questions import Test_Status

ErrorMsg =''
Test_Completed = 0
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            CurrentRole = db.session.query(Roles.Role_ID,Roles.Role_type,Users.Role_ID)\
                .join(Roles,Roles.Role_ID==Users.Role_ID).filter(Users.Role_ID==current_user.Role_ID).first()
            if CurrentRole.Role_type not in roles:
                return redirect(url_for('Home'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper
    return wrapper



@app.route('/')
def index():
    if not current_user:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
@requires_roles('Admin','Assessor')
def dashboard():
    return render_template("/Admin/dashboard.html",Update_Status=Update_Status())




@app.route('/Update_Status')
def Update_Status():
    TestCompleted = Test_Status.query.filter_by(TestStatus="Completed").count()
    All_Users = Users.query.count()
    OnlineUsers = Users.query.filter_by(User_Status=1).count()
    AllTests = Test_Status.query.count()
    Unique_Nationaities = db.session.query(Users.Nationality).distinct().count()
    if AllTests >0:
        Test_info_Percent = (TestCompleted/AllTests)*100
    else:
        Test_info_Percent=0
    if OnlineUsers >0:
        Online_Users_Percent = (OnlineUsers/All_Users)*100
    else:
        Online_Users_Percent=0
    return jsonify(Test_info_Percent=Test_info_Percent,
                   AllTests=AllTests,
                   TestsCompleted=TestCompleted,
                   All_Users=All_Users,
                   OnlineUsers=OnlineUsers,
                   Online_Users_Percent=Online_Users_Percent,
                   Unique_Nationaities=Unique_Nationaities)



@app.route('/logout')
@login_required
def logout():
    User = Users.query.filter_by(UserName=current_user.UserName).first()
    User.User_Status = 2
    db.session.commit()
    logout_user()
    return redirect(url_for('Home'))


@app.route('/register', methods=['GET','POST'])
def RegisterUser():
    ErrorMsg=''
    if request.method =='POST':
        SurName = request.form['FirstName']
        OtherNames = request.form['LastName']
        Nationality = request.form['Nationality']
        UserName = request.form['UserName']
        DoB = request.form['DoB']
        PhoneNumber = request.form['PhoneNumber']
        Email = request.form['Email']
        Gender = request.form['Gender']
        Password = request.form['newPassword']
        print("Data: ", SurName," - ",OtherNames," - ",UserName," - ",PhoneNumber," - ",Email," - ",Gender," - ",Password)
        ExistingUser=Users.query.filter(or_(Users.EmailAddress==Email , Users.UserName==UserName)).first()
        if not ExistingUser:
            print("Not in DB")
            NewUser = Users(
                Sur_Name=SurName,
                EmailAddress=Email,
                UserName=UserName,
                Other_Names=OtherNames,
                GenderID=Gender,
                Nationality=Nationality,
                Role_ID=2,
                DoB=DoB,
                User_Status=2,
                img="avatar.png",
                Pass_word= sha256_crypt.encrypt(Password),
                Date_Created=datetime.now()
            )
            db.session.add(NewUser)
            db.session.commit()
            ErrorMsg="User "+UserName+" Registered Successfully Please check your Email: "+Email+" to activate your account"
            return render_template('/Clients/Success.html',ErrorMsg=ErrorMsg)
        else:
            print("Username or Email Exisit")
            ErrorMsg = "UserName Exists"
            return render_template('/Clients/Register.html',ErrorMsg=ErrorMsg)
    else:
        return render_template('/Clients/Register.html', ErrorMsg=ErrorMsg)


@app.route('/Login', methods=['GET','POST'])
def UserLogin():
    ErrorMsg = ''
    if current_user.is_active:
        print("User is logged in: "+str(current_user.Role_ID))
        if current_user.Role_ID==1 or current_user.Role_ID==3:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('Home'))
    else:
        if request.method == 'POST':
            UserName = request.form['UserName']
            Pass = request.form['PassWord']
            user = Users.query.filter(or_(Users.EmailAddress==UserName , Users.UserName==UserName)).first()
            if not user:
                ErrorMsg = "Wrong UserName"
                return render_template('/Clients/index.html', ErrorMsg=ErrorMsg)
            else:
                if sha256_crypt.verify(Pass, user.Pass_word):
                    if user.User_Status == 2 or user.User_Status == 1:
                        login_user(user)
                        LoggedUser = Users.query.filter_by(UserName=current_user.UserName).first()
                        LoggedUser.User_Status = 1
                        db.session.commit()
                        if LoggedUser.Role_ID == 1 or LoggedUser.Role_ID==3:
                            session.permanent = True
                            return redirect(url_for('dashboard'))
                        elif LoggedUser.Role_ID == 2:
                            session.permanent = True
                            return redirect(url_for('Home'))
                    if user.User_Status == 3:
                        ErrorMsg = "User Locked"
                        return render_template('/Clients/index.html', ErrorMsg=ErrorMsg)
                    if user.User_Status == 4:
                        ErrorMsg = "User is banned"
                        return render_template('/Clients/index.html', ErrorMsg=ErrorMsg)
                    if user.User_Status == 5:
                        ErrorMsg = "User Is suspended"
                        return render_template('/Clients/index.html', ErrorMsg=ErrorMsg)
                else:
                    ErrorMsg = "Wrong Passord...."
        return render_template('/Clients/index.html', ErrorMsg=ErrorMsg)


@app.route('/register')
def registerUser():
    return render_template("/Clients/Register.html")

