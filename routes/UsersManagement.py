from datetime import datetime
import time
import re

from flask_security import UserMixin, RoleMixin
from sqlalchemy import Integer, or_

from src.DBConnect import *
from flask_login import login_required, current_user

from src.models.Admin import *
from src.models.Questions import *
from src.models.Results import *
from src.routes.Login import requires_roles


@app.route('/CouncelorsManagement',methods=['GET','POST'])
@login_required
@requires_roles('Admin')
def loadClients():
    Client_list=''
    CounselorID=''
    if request.method=='POST':
        CounselorID = str(re.sub('[^0-9]+', '',request.form['Counselor']))
        Client_list = db.session.query(Users.EmailAddress,
                                     Users.id,
                                     Users.Sur_Name,
                                     Users.Other_Names,
                                     Users.User_Status,
                                     User_Status.Status_type,
                                       UserAssignment.AssessorID)\
            .join(User_Status,User_Status.Status_ID==Users.User_Status)\
            .outerjoin(UserAssignment,UserAssignment.UserID==Users.id)\
            .filter(Users.Role_ID==2).distinct()
    else:
        Client_list = db.session.query(Users.EmailAddress,
                                       Users.id,
                                       Users.Sur_Name,
                                       Users.Other_Names,
                                       Users.User_Status,
                                       User_Status.Status_type,
                                       UserAssignment.AssessorID) \
            .join(User_Status, User_Status.Status_ID == Users.User_Status) \
            .outerjoin(UserAssignment, UserAssignment.UserID == Users.id) \
            .filter(Users.Role_ID == 2).distinct()
    Counselor_List= Users.query.filter(Users.Role_ID==3)
    return render_template('Admin/usersAssignments.html',Counselor_List=Counselor_List,Client_list=Client_list, CounselorID=CounselorID)

@app.route('/CounselorAssign',methods=['GET','POST'])
@login_required
@requires_roles('Admin')
def AssignCounselor():
    if request.method=='POST':
        CounselorID = str(re.sub('[^0-9]+', '',request.form['CID']))
        ClientID =str(re.sub('[^0-9]+', '',request.form['UID']))
        print(CounselorID, " --- ",ClientID)
        Assignee = UserAssignment.query.filter(UserAssignment.UserID==ClientID).first()
        if ClientID=='' or CounselorID=='':
            return redirect(url_for('loadClients'))
        if not Assignee:
            Client_to_Counselor =UserAssignment(
                UserID=ClientID,
                AssessorID=CounselorID,
                AssignerID=current_user.id,
                timestamp=datetime.now()
            )
            db.session.add(Client_to_Counselor)
        else:
            print(str(Assignee.AssessorID)+" :Exist and Assign "+CounselorID)
            Assignee.AssessorID=CounselorID
        db.session.commit()
        flash("User Assigned to counselor successfully")
    return redirect(url_for('loadClients'))

@app.route('/TestAssign',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def AsignTests():
    Status = ''
    if request.method=='POST':
        TestSelected = request.form.getlist('TestSelected')
        UID = str(re.sub('[^0-9]+', '',request.form['UID']))
        for T in TestSelected:
            TestToAssign = db.session.query(Test_Assignments.TestID).filter(Test_Assignments.TestID==T)\
                .filter(Test_Assignments.UserID==UID).first()
            print(UID+"- Assigned Test -", T)
            if not TestToAssign:
                AssignTest= Test_Assignments(
                    AdminID=current_user.id,
                    UserID=UID,
                    TestID=T,
                    timestamp=datetime.now()
                )
                db.session.add(AssignTest)
                db.session.commit()
                flash("Test Assigned Successfully")
            else:
                flash("Test Alreasy Assigned selected person")
    User_List = db.session.query(Users.id, Users.EmailAddress, Users.Sur_Name, Users.Other_Names, Users.User_Status,
                                 User_Status.Status_type,UserAssignment.AssessorID) \
        .join(User_Status, User_Status.Status_ID == Users.User_Status)\
        .join(UserAssignment,UserAssignment.UserID==Users.id) \
        .filter(UserAssignment.AssessorID==current_user.id)
    Tests_Lists = db.session.query(Tests.ID, Tests.TestType, Tests.Name, Tests.Description).all()
    Assigned_Tests_Lists = db.session.query(Tests.ID, Tests.Name, Tests.TestType, Tests.Description,Test_Assignments.UserID,Test_Assignments.UID)\
        .join(Test_Assignments,Test_Assignments.TestID==Tests.ID).all()

    return render_template('Admin/TestAssignment.html',User_List=User_List,Assigned_Tests_Lists=Assigned_Tests_Lists,Tests_Lists=Tests_Lists, Status=Status)


@app.route('/TestUnAssign',methods=['GET','POST'])
@login_required
@requires_roles('Admin')
def UnAsignTests():
    if request.method=='POST':
        TestSelected = request.form.getlist('TestSelected')
        for T in TestSelected:
            UnMatchTest=Test_Assignments.query.filter_by(UID=T).first()
            db.session.delete(UnMatchTest)
            db.session.commit()
        flash("Test UnAssigned Successfully")
    return redirect(url_for('AsignTests'))