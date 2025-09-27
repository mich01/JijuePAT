from collections import Counter
from datetime import datetime
import time
from werkzeug.utils import secure_filename

from flask_security import UserMixin, RoleMixin
from sqlalchemy import Integer, func

from src.DBConnect import *
from flask_login import login_required, current_user

import re

from src.models.Admin import *
from src.models.Questions import *
from src.models.Results import *
from src.routes.Login import requires_roles

Status =''
#To Populate The Data structure
def PopulateResults(DBResults):
    Temp=[]
    for R in DBResults:
        Temp.append({"TestID":R.TestID,
                     "TestName":R.Name,
                     "TestType":R.TestType,
                     "Agreeableness":R.Agreeableness,
                     "Openess_to_Experience":R.Openess_to_Experience,
                     "Consientious":R.Consientious,
                     "Extraversion":R.Extraversion,
                     "Neuroticism":R.Neuroticism})
    return Temp




def ComputeFinalSCores(InputList):
    Temp=[]
    Exists = False
    TempID = 0
    for X in InputList:
        Exists=False
        if not Temp:
            Temp.append({"TestID": X['TestID'],
                         "TestName": X['TestName'],
                         "TestType": X['TestType'],
                         "Agreeableness": X['Agreeableness'],
                         "Openess_to_Experience": X['Openess_to_Experience'],
                         "Consientious": X['Consientious'],
                         "Extraversion": X['Extraversion'],
                         "Neuroticism": X['Neuroticism']})
        else:
            for T in Temp:
                if T['TestID']==X['TestID']:
                    Exists=True
                    TempID= X['TestID']
            if Exists == True:
                for I in Temp:
                    if I['TestID']==TempID:
                        I['Agreeableness'] = I['Agreeableness'] + int(X['Agreeableness'])
                        I['Openess_to_Experience'] = I['Openess_to_Experience'] + int(X['Openess_to_Experience'])
                        I['Consientious'] = I['Consientious'] + X['Consientious']
                        I['Extraversion'] = I['Extraversion'] + int(X['Extraversion'])
                        I['Neuroticism'] = I['Neuroticism'] + int(X['Neuroticism'])
                        Exists = False
            else:
                Temp.append({"TestID": X['TestID'],
                             "TestName": X['TestName'],
                             "TestType": X['TestType'],
                             "Agreeableness": X['Agreeableness'],
                             "Openess_to_Experience": X['Openess_to_Experience'],
                             "Consientious": X['Consientious'],
                             "Extraversion": X['Extraversion'],
                             "Neuroticism": X['Neuroticism']})
        Exists = False
    return Temp

def AverageResults(Count, InputList):
    for I in InputList:
        for c in Count:
            if  I['TestName']==c:
                I['Agreeableness'] = int(I['Agreeableness'] /Count[c])
                I['Openess_to_Experience'] = int(I['Openess_to_Experience'] /Count[c])
                I['Consientious'] = int( I['Consientious'] /Count[c])
                I['Extraversion'] =int( I['Extraversion'] /Count[c])
                I['Neuroticism'] = int( I['Neuroticism'] /Count[c])
    return InputList




@app.route('/Summary',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def SummaryResultsModule():
    if current_user.Role_ID==3:
        UserSummary= db.session.query(Test_Status.UserID,
                                      Test_Status.TestID,
                                      Test_Status.DateStarted,
                                      Test_Assignments.AdminID,
                                      Test_Status.DateCompleted,
                                      Tests.Name,
                                      Test_Status.TestStatus,
                                      Users.Sur_Name,
                                      Users.Other_Names,
                                      Users.EmailAddress)\
            .join(Users,Users.id==Test_Status.UserID)\
            .join(Tests,Tests.ID==Test_Status.TestID)\
            .join(Test_Assignments,Test_Assignments.UserID==Test_Status.UserID)\
            .filter(Test_Assignments.AdminID==current_user.id).distinct()

        UserTests = db.session.query(Test_Assignments.TestID,Tests.Name,Tests.TestType).join(Tests,Tests.ID==Test_Assignments.TestID)\
            .filter(Test_Assignments.AdminID==current_user.id)
    else:
        UserSummary = db.session.query(Test_Status.UserID,
                                   Test_Status.TestID,
                                   Test_Status.DateStarted,
                                   Test_Status.DateCompleted,
                                   Tests.Name,
                                   Test_Status.TestStatus,
                                   Users.Sur_Name,
                                   Users.Other_Names,
                                   Users.EmailAddress)\
            .join(Users,Users.id==Test_Status.UserID)\
            .join(Tests,Tests.ID==Test_Status.TestID)

        UserTests = db.session.query(Test_Assignments.TestID, Tests.Name, Tests.TestType)\
            .join(Tests,Tests.ID == Test_Assignments.TestID).distinct()
    return render_template('Admin/Analysis/SummaryResults.html',
                           UserTests=UserTests,
                           UserSummary=UserSummary)

@app.route('/AnxietyResults',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def AnxietyResults():
    TestList = []
    AverageSummary = []
    if current_user.Role_ID == 3:
        Anxiety_Summary = db.session.query(SummaryResults.UserID,
                                           SummaryResults.TestID,
                                           SummaryResults.Anxiety,
                                           Tests.Name,
                                           Users.id,
                                           Users.Sur_Name,
                                           Users.Other_Names,
                                           UserAssignment.UserID,
                                           UserAssignment.AssessorID)\
            .join(Users, Users.id==SummaryResults.UserID)\
            .join(Tests, Tests.ID==SummaryResults.TestID)\
            .join(UserAssignment,UserAssignment.UserID==SummaryResults.UserID)\
            .filter(SummaryResults.Anxiety>0)\
            .filter(UserAssignment.AssessorID==current_user.id)
        for T in Anxiety_Summary:
            TestList.append(T.Name)
        TestIDs = []
        for I in Anxiety_Summary:
            TestIDs.append(I.TestID)
        UniqueTests = set(TestIDs)
        for X in UniqueTests:
            print("UserID: " +str(X))
            AverageSummary.append(db.session.query(Test_Assignments.TestID,
                                                   Test_Assignments.AdminID,
                                                   Tests.Name,
                                                   func.max(SummaryResults.Anxiety).label("Max_Score")
                                                   , func.min(SummaryResults.Anxiety).label("Min_Score")
                                                   , func.avg(SummaryResults.Anxiety).label("Avg_Score"),
                                                   func.count().label("Counts")) \
                                  .join(SummaryResults, SummaryResults.TestID == Test_Assignments.TestID) \
                                  .join(Tests, Tests.ID == Test_Assignments.TestID) \
                                  .filter(SummaryResults.TestID == X)
                                  .filter(SummaryResults.Anxiety > 0).filter(Test_Assignments.AdminID==current_user.id))
    else:
        Anxiety_Summary = db.session.query(SummaryResults.UserID,
                                           SummaryResults.TestID,
                                           SummaryResults.Anxiety,
                                           Tests.Name,
                                           Users.id,
                                           Users.Sur_Name,
                                           Users.Other_Names,
                                           UserAssignment.UserID,
                                           UserAssignment.AssessorID) \
            .join(Users, Users.id == SummaryResults.UserID) \
            .join(Tests, Tests.ID == SummaryResults.TestID) \
            .filter(SummaryResults.Anxiety > 0) \
            .join(UserAssignment, UserAssignment.UserID == SummaryResults.UserID)
        for T in Anxiety_Summary:
            TestList.append(T.Name)
        TestIDs = []
        for I in Anxiety_Summary:
            TestIDs.append(I.TestID)
        UniqueTests = set(TestIDs)
        for X in UniqueTests:
            print(X)
            AverageSummary.append(db.session.query(Test_Assignments.TestID, Tests.Name,
                                                   func.max(SummaryResults.Anxiety).label("Max_Score")
                                                   , func.min(SummaryResults.Anxiety).label("Min_Score")
                                                   , func.avg(SummaryResults.Anxiety).label("Avg_Score"),
                                                   func.count().label("Counts")) \
                                  .join(SummaryResults, SummaryResults.TestID == Test_Assignments.TestID) \
                                  .join(Tests, Tests.ID == Test_Assignments.TestID) \
                                  .filter(SummaryResults.TestID == X).filter(SummaryResults.Anxiety > 0))
    Count = len(AverageSummary)
    MaxValues = []
    MinValues = []
    AvgValues = []
    Min=0
    Max=0
    Avg=0
    if Count > 0:
        for T in AverageSummary:
            for V in T:
                if V.Max_Score != None and V.Min_Score != None and V.Avg_Score != None:
                    print("Hello: " + str(V.Max_Score) + "Hello: " + str(V.Min_Score) + "Hello: " + str(V.Avg_Score))
                    MaxValues.append(V.Max_Score)
                    MinValues.append(V.Min_Score)
                    AvgValues.append(V.Avg_Score)
        if MaxValues and MinValues and AvgValues:
            Max = max(MaxValues)
            Min = min(MinValues)
            Avg = sum(AvgValues) / Count
    return render_template('Admin/Analysis/AnxietyResults.html',
                           AverageSummary=AverageSummary,
                           Max=Max,
                           Min=Min,
                           Avg=Avg,
                           Count=Count,
                           Anxiety_Summary=Anxiety_Summary)

@app.route('/AngerResults',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def AngerResults():
    TestList=[]
    AverageSummary=[]
    if current_user.Role_ID == 3:
        Anger_Summary = db.session.query(SummaryResults.UserID,
                                           SummaryResults.TestID,
                                           SummaryResults.Anger,
                                           Tests.Name,
                                           Users.id,
                                           Users.Sur_Name,
                                           Users.Other_Names,
                                           UserAssignment.UserID,
                                           UserAssignment.AssessorID)\
            .join(Users, Users.id==SummaryResults.UserID)\
            .join(Tests, Tests.ID==SummaryResults.TestID)\
            .join(UserAssignment,UserAssignment.UserID==SummaryResults.UserID)\
            .filter(SummaryResults.Anger > 0)\
            .filter(UserAssignment.AssessorID==current_user.id)
        for T in Anger_Summary:
            TestList.append(T.Name)
        TestIDs = []
        for I in Anger_Summary:
            TestIDs.append(I.TestID)
        UniqueTests = set(TestIDs)
        for X in UniqueTests:
            print("UserID: " +str(X))
            AverageSummary.append(db.session.query(Test_Assignments.TestID,
                                                   Test_Assignments.AdminID,
                                                   Tests.Name,
                                                   func.max(SummaryResults.Anger).label("Max_Score")
                                                   , func.min(SummaryResults.Anger).label("Min_Score")
                                                   , func.avg(SummaryResults.Anger).label("Avg_Score"),
                                                   func.count().label("Counts")) \
                                  .join(SummaryResults, SummaryResults.TestID == Test_Assignments.TestID) \
                                  .join(Tests, Tests.ID == Test_Assignments.TestID) \
                                  .filter(SummaryResults.TestID == X)
                                  .filter(SummaryResults.Anger > 0).filter(Test_Assignments.AdminID==current_user.id))
    else:
        Anger_Summary = db.session.query(SummaryResults.UserID,
                                           SummaryResults.TestID,
                                           SummaryResults.Anger,
                                           Tests.Name,
                                           Users.id,
                                           Users.Sur_Name,
                                           Users.Other_Names,
                                           UserAssignment.UserID,
                                           UserAssignment.AssessorID) \
            .join(Users, Users.id == SummaryResults.UserID) \
            .join(Tests, Tests.ID == SummaryResults.TestID) \
            .join(UserAssignment, UserAssignment.UserID == SummaryResults.UserID)\
            .filter(SummaryResults.Anger > 0)
        for T in Anger_Summary:
            TestList.append(T.Name)
        TestIDs = []
        for I in Anger_Summary:
            TestIDs.append(I.TestID)
        UniqueTests = set(TestIDs)
        for X in UniqueTests:
            print(X)
            AverageSummary.append(db.session.query(Test_Assignments.TestID, Tests.Name,
                                                   func.max(SummaryResults.Anger).label("Max_Score")
                                                   , func.min(SummaryResults.Anger).label("Min_Score")
                                                   , func.avg(SummaryResults.Anger).label("Avg_Score"),
                                                   func.count().label("Counts")) \
                                  .join(SummaryResults, SummaryResults.TestID == Test_Assignments.TestID) \
                                  .join(Tests, Tests.ID == Test_Assignments.TestID) \
                                  .filter(SummaryResults.TestID == X).filter(SummaryResults.Anger > 0))
    Count = len(AverageSummary)
    MaxValues = []
    MinValues = []
    AvgValues = []
    Min=0
    Max=0
    Avg=0
    if Count > 0:
        for T in AverageSummary:
            for V in T:
                if V.Max_Score != None and V.Min_Score != None and V.Avg_Score != None:
                    print("Hello: " + str(V.Max_Score) + "Hello: " + str(V.Min_Score) + "Hello: " + str(V.Avg_Score))
                    MaxValues.append(V.Max_Score)
                    MinValues.append(V.Min_Score)
                    AvgValues.append(V.Avg_Score)
        if MaxValues and MinValues and AvgValues:
            Max = max(MaxValues)
            Min = min(MinValues)
            Avg = sum(AvgValues) / Count
    return render_template('Admin/Analysis/AngerResults.html',
                           Max=Max,
                           Min=Min,
                           Avg=Avg,
                           Count=Count,
                           AverageSummary=AverageSummary,
                           Anger_Summary=Anger_Summary)

@app.route('/DepressionResults',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def DepressionResults():
    TestList=[]
    AverageSummary=[]
    if current_user.Role_ID == 3:
        Depression_Summary = db.session.query(SummaryResults.UserID,
                                         SummaryResults.TestID,
                                         SummaryResults.Depression,
                                         Tests.Name,
                                         Users.id,
                                         Users.Sur_Name,
                                         Users.Other_Names,
                                         UserAssignment.UserID,
                                         UserAssignment.AssessorID) \
            .join(Users, Users.id == SummaryResults.UserID) \
            .join(Tests, Tests.ID == SummaryResults.TestID) \
            .join(UserAssignment, UserAssignment.UserID == SummaryResults.UserID) \
            .filter(SummaryResults.Depression > 0)\
            .filter(UserAssignment.AssessorID == current_user.id)
        for T in Depression_Summary:
            TestList.append(T.Name)
        TestIDs = []
        for I in Depression_Summary:
            TestIDs.append(I.TestID)
        UniqueTests = set(TestIDs)
        for X in UniqueTests:
            print("UserID: " + str(X))
            AverageSummary.append(db.session.query(Test_Assignments.TestID,
                                                   Test_Assignments.AdminID,
                                                   Tests.Name,
                                                   func.max(SummaryResults.Depression).label("Max_Score")
                                                   , func.min(SummaryResults.Depression).label("Min_Score")
                                                   , func.avg(SummaryResults.Depression).label("Avg_Score"),
                                                   func.count().label("Counts")) \
                                  .join(SummaryResults, SummaryResults.TestID == Test_Assignments.TestID) \
                                  .join(Tests, Tests.ID == Test_Assignments.TestID) \
                                  .filter(SummaryResults.TestID == X)
                                  .filter(SummaryResults.Depression > 0).filter(
                Test_Assignments.AdminID == current_user.id))
    else:
        Depression_Summary = db.session.query(SummaryResults.UserID,
                                         SummaryResults.TestID,
                                         SummaryResults.Depression,
                                         Tests.Name,
                                         Users.id,
                                         Users.Sur_Name,
                                         Users.Other_Names,
                                         UserAssignment.UserID,
                                         UserAssignment.AssessorID) \
            .join(Users, Users.id == SummaryResults.UserID) \
            .join(Tests, Tests.ID == SummaryResults.TestID) \
            .join(UserAssignment, UserAssignment.UserID == SummaryResults.UserID)\
            .filter(SummaryResults.Depression > 0)
        for T in Depression_Summary:
            TestList.append(T.Name)
        TestIDs = []
        for I in Depression_Summary:
            TestIDs.append(I.TestID)
        UniqueTests = set(TestIDs)
        for X in UniqueTests:
            print(X)
            AverageSummary.append(db.session.query(Test_Assignments.TestID, Tests.Name,
                                                   func.max(SummaryResults.Depression).label("Max_Score")
                                                   , func.min(SummaryResults.Depression).label("Min_Score")
                                                   , func.avg(SummaryResults.Depression).label("Avg_Score"),
                                                   func.count().label("Counts")) \
                                  .join(SummaryResults, SummaryResults.TestID == Test_Assignments.TestID) \
                                  .join(Tests, Tests.ID == Test_Assignments.TestID) \
                                  .filter(SummaryResults.TestID == X).filter(SummaryResults.Depression > 0))
    Count = len(AverageSummary)
    MaxValues = []
    MinValues = []
    AvgValues = []
    Min = 0
    Max = 0
    Avg = 0
    if Count > 0:
        for T in AverageSummary:
            for V in T:
                if V.Max_Score!=None and V.Min_Score !=None and V.Avg_Score!=None:
                    print("Hello: " + str(V.Max_Score)+"Hello: " + str(V.Min_Score)+"Hello: " + str(V.Avg_Score))
                    MaxValues.append(V.Max_Score)
                    MinValues.append(V.Min_Score)
                    AvgValues.append(V.Avg_Score)
        if MaxValues and MinValues and AvgValues:
            Max = max(MaxValues)
            Min = min(MinValues)
            Avg = sum(AvgValues) / Count
    return render_template('Admin/Analysis/DepressionResults.html',
                           AverageSummary=AverageSummary,
                           Max=Max,
                           Min=Min,
                           Avg=Avg,
                           Count=Count,
                           Depression_Summary=Depression_Summary)


@app.route('/IQResults',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def IQResults():
    TestList=[]
    AverageSummary = []
    if current_user.Role_ID == 3:
        IQ_Summary = db.session.query(SummaryResults.UserID,
                                         SummaryResults.TestID,
                                         SummaryResults.IQ,
                                         Tests.Name,
                                         Users.id,
                                         Users.Sur_Name,
                                         Users.Other_Names,
                                         UserAssignment.UserID,
                                         UserAssignment.AssessorID) \
            .join(Users, Users.id == SummaryResults.UserID) \
            .join(Tests, Tests.ID == SummaryResults.TestID) \
            .join(UserAssignment, UserAssignment.UserID == SummaryResults.UserID) \
            .filter(SummaryResults.IQ>0)\
            .filter(UserAssignment.AssessorID == current_user.id)
        for T in IQ_Summary:
            TestList.append(T.Name)
        TestIDs = []
        for I in IQ_Summary:
            TestIDs.append(I.TestID)
        UniqueTests = set(TestIDs)
        for X in UniqueTests:
            print("UserID: " + str(X))
            AverageSummary.append(db.session.query(Test_Assignments.TestID,
                                                   Test_Assignments.AdminID,
                                                   Tests.Name,
                                                   func.max(SummaryResults.IQ).label("Max_Score")
                                                   , func.min(SummaryResults.IQ).label("Min_Score")
                                                   , func.avg(SummaryResults.IQ).label("Avg_Score"),
                                                   func.count().label("Counts")) \
                                  .join(SummaryResults, SummaryResults.TestID == Test_Assignments.TestID) \
                                  .join(Tests, Tests.ID == Test_Assignments.TestID) \
                                  .filter(SummaryResults.TestID == X)
                                  .filter(SummaryResults.IQ > 0).filter(
                Test_Assignments.AdminID == current_user.id))
    else:
        IQ_Summary = db.session.query(SummaryResults.UserID,
                                         SummaryResults.TestID,
                                         SummaryResults.IQ,
                                         Tests.Name,
                                         Users.id,
                                         Users.Sur_Name,
                                         Users.Other_Names,
                                         UserAssignment.UserID,
                                         UserAssignment.AssessorID) \
            .join(Users, Users.id == SummaryResults.UserID) \
            .join(Tests, Tests.ID == SummaryResults.TestID) \
            .join(UserAssignment, UserAssignment.UserID == SummaryResults.UserID)\
            .filter(SummaryResults.IQ>0)
        for T in IQ_Summary:
            TestList.append(T.Name)
        TestIDs = []
        for I in IQ_Summary:
            TestIDs.append(I.TestID)
        UniqueTests = set(TestIDs)
        for X in UniqueTests:
            print(X)
            AverageSummary.append(db.session.query(Test_Assignments.TestID, Tests.Name,
                                                   func.max(SummaryResults.IQ).label("Max_Score")
                                                   , func.min(SummaryResults.IQ).label("Min_Score")
                                                   , func.avg(SummaryResults.IQ).label("Avg_Score"),
                                                   func.count().label("Counts")) \
                                  .join(SummaryResults, SummaryResults.TestID == Test_Assignments.TestID) \
                                  .join(Tests, Tests.ID == Test_Assignments.TestID) \
                                  .filter(SummaryResults.TestID == X).filter(SummaryResults.IQ > 0))
    MaxValues=[]
    MinValues=[]
    AvgValues=[]
    Min = 0
    Max = 0
    Avg = 0
    Count = len(AverageSummary)
    if Count > 0:
        for T in AverageSummary:
            for V in T:
                if V.Max_Score != None and V.Min_Score != None and V.Avg_Score != None:
                    print("Hello: " + str(V.Max_Score) + "Hello: " + str(V.Min_Score) + "Hello: " + str(V.Avg_Score))
                    MaxValues.append(V.Max_Score)
                    MinValues.append(V.Min_Score)
                    AvgValues.append(V.Avg_Score)
        if MaxValues and MinValues and AvgValues:
            Max = max(MaxValues)
            Min = min(MinValues)
            Avg = sum(AvgValues) / Count
    return render_template('Admin/Analysis/IQResults.html',
                           AverageSummary=AverageSummary,
                           Max=Max,
                           Min=Min,
                           Avg=Avg,
                           Count=Count,
                           IQ_Summary=IQ_Summary)


@app.route('/PTSD',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def PTSDResults():
    TestList=[]
    AverageSummary = []
    if current_user.Role_ID == 3:
        PTSD_Summary = db.session.query(SummaryResults.UserID,
                                        SummaryResults.TestID,
                                        SummaryResults.PTSD,
                                        Tests.Name,
                                        Users.id,
                                        Users.Sur_Name,
                                        Users.Other_Names,
                                        UserAssignment.UserID,
                                        UserAssignment.AssessorID) \
            .join(Users, Users.id == SummaryResults.UserID) \
            .join(Tests, Tests.ID == SummaryResults.TestID) \
            .join(UserAssignment, UserAssignment.UserID == SummaryResults.UserID)\
            .filter(SummaryResults.PTSD > 0)\
            .filter(UserAssignment.AssessorID == current_user.id)
        for T in PTSD_Summary:
            TestList.append(T.Name)
        TestIDs = []
        for I in PTSD_Summary:
            TestIDs.append(I.TestID)
        UniqueTests = set(TestIDs)
        for X in UniqueTests:
            print("UserID: " + str(X))
            AverageSummary.append(db.session.query(Test_Assignments.TestID,
                                                   Test_Assignments.AdminID,
                                                   Tests.Name,
                                                   func.max(SummaryResults.PTSD).label("Max_Score")
                                                   , func.min(SummaryResults.PTSD).label("Min_Score")
                                                   , func.avg(SummaryResults.PTSD).label("Avg_Score"),
                                                   func.count().label("Counts")) \
                .join(SummaryResults, SummaryResults.TestID == Test_Assignments.TestID) \
                .join(Tests, Tests.ID == Test_Assignments.TestID) \
                .filter(SummaryResults.TestID == X)
                .filter(SummaryResults.PTSD > 0).filter(
                Test_Assignments.AdminID == current_user.id))
    else:
        PTSD_Summary = db.session.query(SummaryResults.UserID,
                                        SummaryResults.TestID,
                                        SummaryResults.PTSD,
                                        Tests.Name,
                                        Users.id,
                                        Users.Sur_Name,
                                        Users.Other_Names,
                                        UserAssignment.UserID,
                                        UserAssignment.AssessorID) \
            .join(Users, Users.id == SummaryResults.UserID) \
            .join(Tests, Tests.ID == SummaryResults.TestID) \
            .join(UserAssignment, UserAssignment.UserID == SummaryResults.UserID)\
            .filter(SummaryResults.PTSD > 0)
        for T in PTSD_Summary:
            TestList.append(T.Name)
        TestIDs = []
        for I in PTSD_Summary:
            TestIDs.append(I.TestID)
        UniqueTests = set(TestIDs)
        for X in UniqueTests:
            print(X)
            AverageSummary.append(db.session.query(Test_Assignments.TestID, Tests.Name,
                                                   func.max(SummaryResults.PTSD).label("Max_Score")
                                                   , func.min(SummaryResults.PTSD).label("Min_Score")
                                                   , func.avg(SummaryResults.PTSD).label("Avg_Score"),
                                                   func.count().label("Counts")) \
                                  .join(SummaryResults, SummaryResults.TestID == Test_Assignments.TestID) \
                                  .join(Tests, Tests.ID == Test_Assignments.TestID) \
                                  .filter(SummaryResults.TestID == X).filter(SummaryResults.PTSD > 0))
    MaxValues = []
    MinValues = []
    AvgValues = []
    Min = 0
    Max = 0
    Avg = 0
    Count = len(AverageSummary)
    if Count > 0:
        for T in AverageSummary:
            for V in T:
                if V.Max_Score != None and V.Min_Score != None and V.Avg_Score != None:
                    print("Hello: " + str(V.Max_Score) + "Hello: " + str(V.Min_Score) + "Hello: " + str(V.Avg_Score))
                    MaxValues.append(V.Max_Score)
                    MinValues.append(V.Min_Score)
                    AvgValues.append(V.Avg_Score)
        if MaxValues and MinValues and AvgValues:
            Max = max(MaxValues)
            Min = min(MinValues)
            Avg = sum(AvgValues) / Count
    return render_template('Admin/Analysis/PTSDResults.html',
                           AverageSummary=AverageSummary,
                           Max=Max,
                           Min=Min,
                           Avg=Avg,
                           Count=Count,
                           PTSD_Summary=PTSD_Summary)

@app.route('/ResultsModule')
@login_required
@requires_roles('Admin')
def ResultsModule():
    Summary = db.session.query(SummaryResults.TestID,
                               SummaryResults.timestamp,
                               SummaryResults.Agreeableness,
                               SummaryResults.Consientious,
                               SummaryResults.Extraversion,
                               SummaryResults.Neuroticism,
                               SummaryResults.UID,
                               SummaryResults.UserID,
                               SummaryResults.Openess_to_Experience,
                               SummaryResults.timestamp,
                               Users.UserName,
                               Tests.Name)\
        .join(Users,Users.id==SummaryResults.TestID)\
        .join(Tests,Tests.ID==SummaryResults.TestID)

    return render_template('Admin/Analysis/IndividualResults.html',Summary=Summary)



@app.route('/IndividualResults',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def IndividualResults():
    AnxietyTestQuestions = 0


    UserProfile=''
    UserPersonality=''
    UserResults=''
    Personality = 1
    Anxiety = 1
    IQ = 1
    Depression = 1
    PTSD = 1
    AngetMmanagement = 1

    Volatility=0
    Extraversion = 0
    Agreeableness = 0
    Consientious = 0
    Compassion = 0
    Politeness = 0
    Neuroticism = 0
    Industriousness = 0
    Orderliness = 0
    Enthusiasm = 0
    Assertiveness = 0
    Withdrawal = 0
    Openess_to_Experience = 0
    Openness =0
    Intellect=0

    AvgAnxiety = 0
    AvgIQ = 0
    AvgDepression = 0
    AvgPTSD = 0
    AvgAngetMmanagement = 0
    if current_user.Role_ID==3:
        User_List = db.session.query(UserAssignment.AssessorID,
                                     UserAssignment.UserID,
                                     Users.id,
                                     Users.Sur_Name,
                                     Users.Other_Names)\
            .join(Users,Users.id==UserAssignment.UserID)\
            .filter(UserAssignment.AssessorID==current_user.id).distinct()
    else:
        User_List = db.session.query(UserAssignment.AssessorID,
                                     UserAssignment.UserID,
                                     Users.id,
                                     Users.Sur_Name,
                                     Users.Other_Names) \
            .join(Users, Users.id == UserAssignment.UserID).distinct()
    if request.method=='POST':
        UserID = request.form['UserSelected']
        UserProfile = db.session.query(Users.GenderID,
                                       Users.img,
                                       Users.id,
                                       Users.Other_Names,
                                       Users.Sur_Name,
                                       Users.EmailAddress,
                                       Users.Nationality,
                                       Users.DoB,
                                       Users.GenderID,
                                       Gender.Gender)\
            .join(Gender, Gender.ID == Users.GenderID).filter(Users.id == UserID).first()

        print(UserProfile.GenderID)
        UserPersonality = db.session.query(Tests.Name,Tests.ID,Tests.TestType,
            Test_Status.TestStatus)\
            .join(Tests,Tests.ID==Test_Status.TestID).filter(Test_Status.UserID==UserID)

        UserResults = db.session.query(SummaryResults.TestID,
                                         SummaryResults.PTSD,
                                       SummaryResults.Extraversion,
                                       SummaryResults.Agreeableness,
                                       SummaryResults.Consientious,
                                       SummaryResults.Compassion,
                                       SummaryResults.Politeness,
                                       SummaryResults.Neuroticism,
                                       SummaryResults.Anger,
                                       SummaryResults.PTSD,
                                       SummaryResults.Anxiety,
                                       SummaryResults.Depression,
                                       SummaryResults.IQ,
                                       SummaryResults.Industriousness,
                                       SummaryResults.Orderliness,
                                       SummaryResults.Enthusiasm,
                                       SummaryResults.Assertiveness,
                                       SummaryResults.Withdrawal,
                                       SummaryResults.Volatility,
                                       SummaryResults.Intellect,
                                       SummaryResults.Openess_to_Experience,
                                       SummaryResults.Openness,
                                       SummaryResults.UID,
                                       SummaryResults.UserID,
                                         Tests.Name,
                                       Tests.TestType)\
            .join(Tests,Tests.ID==SummaryResults.TestID).filter(SummaryResults.UserID==UserID)

        #Tests_Taken = db.session.query(Tests.TestType,Tests.Name)
        for P in UserResults:
            if P.TestType == "Personality":
                Personality=Personality+1
                Extraversion = Extraversion+P.Extraversion
                Agreeableness = Agreeableness+P.Agreeableness
                Consientious = Consientious+P.Consientious
                Compassion = Compassion+P.Compassion
                Politeness = Politeness+P.Politeness
                Neuroticism = Neuroticism+P.Neuroticism
                Industriousness = Industriousness+P.Industriousness
                Orderliness = Orderliness+P.Orderliness
                Enthusiasm = Enthusiasm+P.Enthusiasm
                Assertiveness = Assertiveness+P.Assertiveness
                Openness = Openness+P.Openness
                Withdrawal = Withdrawal+P.Withdrawal
                Volatility = Volatility+P.Volatility
                Intellect = Intellect+P.Intellect
                Openess_to_Experience = Openess_to_Experience+P.Openess_to_Experience
                print(P.TestType)
            if P.TestType == "Anxiety":
                Anxiety=Anxiety+1
                AvgAnxiety=AvgAnxiety+P.Anxiety
                print(P.TestType)
            if P.TestType == "IQ":
                IQ=IQ+1
                AvgIQ=AvgIQ+P.IQ
                print(P.TestType)
            if P.TestType == "Depression":
                Depression=Depression+1
                AvgDepression=AvgDepression+P.Depression
                print(P.TestType)
            if P.TestType == "PTSD":
                PTSD=PTSD+1
                AvgPTSD=AvgPTSD+P.PTSD
                print(P.TestType)
            if P.TestType == "AngerManagement":
                AngetMmanagement=AngetMmanagement+1
                AvgAngetMmanagement=AvgAngetMmanagement+P.Anger
                print(P.TestType)
            print(Personality," -- ",Anxiety)

    if Personality>1:
        Personality=Personality-1
    if Anxiety>1:
        Anxiety=Anxiety-1
    if AvgIQ>1:
        IQ=IQ-1
    if Depression>1:
        Depression=Depression-1
    if PTSD>1:
        PTSD=PTSD-1
    if AngetMmanagement>1:
        AngetMmanagement=AngetMmanagement-1

    Extraversion = Extraversion/Personality
    Agreeableness = Agreeableness/Personality
    Consientious = Consientious/Personality
    Compassion = Compassion/Personality
    Politeness = Politeness/Personality
    Neuroticism = Neuroticism/Personality
    Industriousness = Industriousness/Personality
    Orderliness = Orderliness/Personality
    Openness = Openness/Personality
    Enthusiasm = Enthusiasm/Personality
    Assertiveness = Assertiveness/Personality
    Withdrawal = Withdrawal/Personality
    Volatility = Volatility/Personality
    Intellect = Intellect/Personality
    Openess_to_Experience = Openess_to_Experience/Personality


    AvgAnxiety = int(AvgAnxiety/Anxiety)
    AvgIQ = int(AvgIQ/IQ)
    AvgDepression = int(AvgDepression/Depression)
    AvgPTSD = int(AvgPTSD/PTSD)
    AvgAngetMmanagement = int(AvgAngetMmanagement/AngetMmanagement)
    return render_template('Admin/Analysis/IndividualResults.html',
                           AvgIQ=AvgIQ,
                           AvgDepression=AvgDepression,
                           AvgPTSD=AvgPTSD,
                           AvgAngetMmanagement=AvgAngetMmanagement,
                           AvgAnxiety=AvgAnxiety,
                           Extraversion=Extraversion / Personality,
                           Agreeableness = Agreeableness,
                           Consientious = Consientious,
                           Volatility=Volatility,
                           Compassion = Compassion,
                           Politeness = Politeness,
                           Neuroticism = Neuroticism,
                           Industriousness = Industriousness,
                           Orderliness = Orderliness,
                           Enthusiasm = Enthusiasm,
                           Assertiveness = Assertiveness,
                           Withdrawal = Withdrawal,
                           Intellect=Intellect,
                           Openness=Openness,
                           Openess_to_Experience = Openess_to_Experience,
                           UserResults=UserResults,UserProfile=UserProfile,User_List=User_List,UserPersonality=UserPersonality)


@app.route('/IndividualStats',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def Personality_Types_Stats():
    UserPersonality=[]
    UserProfile=''
    User_List = db.session.query(Users.id, Users.Sur_Name, Users.Other_Names) \
        .join(Test_Status, Test_Status.UserID == Users.id) \
        .join(Test_Assignments, Test_Assignments.TestID == Test_Status.TestID) \
        .filter(Test_Assignments.UserID == current_user.id).distinct()
    if request.method=='POST':
        UserID = str(re.sub('[z0-9]+', '',request.form['UserSelected']))
        UserProfile = Users.query.filter_by(id = UserID).first()
        UserPersonality =  db.session.query(
            SummaryResults.Agreeableness,
            SummaryResults.UserID,
            SummaryResults.Consientious,
            SummaryResults.Extraversion,
            SummaryResults.Neuroticism,
            SummaryResults.UID,
            SummaryResults.UserID,
            SummaryResults.Openess_to_Experience,
            Users.img,
            Users.id,Tests.Name)\
            .join(Tests,Tests.ID==SummaryResults.TestID)\
            .join(Users,Users.id==SummaryResults.UserID) \
            .filter(SummaryResults.UserID==UserID)
    return render_template('Admin/Analysis/IndividualResults.html',UserProfile=UserProfile,User_List=User_List,UserPersonality=UserPersonality)


@app.route('/userTests')
@login_required
@requires_roles('Admin','Assessor')
def UserTests():
    if current_user.Role_ID==1:
        Summary = db.session.query(Test_Status.UserID,
                                   Test_Status.TestID,
                                   Test_Status.DateStarted,
                                   Test_Status.DateCompleted,
                                   Tests.Name,
                                   Test_Status.TestStatus,
                                   Users.Sur_Name,
                                   Users.Other_Names,
                                   Users.EmailAddress)\
            .join(Users,Users.id==Test_Status.UserID)\
            .join(Tests,Tests.ID==Test_Status.TestID)
    else:
        Summary = db.session.query(Test_Status.UserID,
                                   Test_Status.TestID,
                                   Test_Status.DateStarted,
                                   Test_Status.DateCompleted,
                                   Tests.Name,
                                   Test_Status.TestStatus,
                                   Users.Sur_Name,
                                   Users.Other_Names,
                                   Users.EmailAddress) \
            .join(Users, Users.id == Test_Status.UserID) \
            .join(Tests, Tests.ID == Test_Status.TestID)\
            .join(Test_Assignments,Test_Assignments.TestID==Tests.ID)\
            .filter(Tests.ID==Test_Assignments.TestID)

    return render_template('Admin/Analysis/UserStats.html',Summary=Summary)



@app.route('/select',methods=['GET','POST'])
@login_required
def select():
    TestID=0
    Attrib=''
    if request.method=='POST':
        ChoiceSelected = request.form['SelectedChoice']
        Attribute = request.form['Attribute']
        QID= request.form['QuestionID']
        TestID= request.form['TestID']
        session['TestID'] = TestID
        print(Attribute," scores ",ChoiceSelected," Question ",QID )
        if TestID!=None:
            SummaryChoice = SummaryResults.query.filter_by(UserID=current_user.id)\
            .filter_by(TestID=TestID).first()
            if Attribute == "Intelect":
                SummaryChoice.Intellect=int(SummaryChoice.Intellect) + int(ChoiceSelected)
            elif Attribute == "Agreeableness":
                SummaryChoice.Agreeableness=int(SummaryChoice.Agreeableness) + int(ChoiceSelected)
            elif Attribute == "Compassion":
                SummaryChoice.Compassion = int(SummaryChoice.Compassion) + int(ChoiceSelected)
            elif Attribute == "Politeness":
                SummaryChoice.Politeness = int(SummaryChoice.Politeness) + int(ChoiceSelected)
            elif Attribute == "Consientious":
                SummaryChoice.Consientious = int(SummaryChoice.Consientious) + int(ChoiceSelected)
            elif Attribute == "Orderliness":
                SummaryChoice.Orderliness = int(SummaryChoice.Orderliness) + int(ChoiceSelected)
            elif Attribute == "Industriousness":
                SummaryChoice.Industriousness = int(SummaryChoice.Industriousness) + int(ChoiceSelected)
            elif Attribute == "Extraversion":
                SummaryChoice.Extraversion = int(SummaryChoice.Extraversion) + int(ChoiceSelected)
            elif Attribute == "Enthusiasm":
                SummaryChoice.Enthusiasm = int(SummaryChoice.Enthusiasm) + int(ChoiceSelected)
            elif Attribute == "Assertiveness":
                SummaryChoice.Assertiveness = int(SummaryChoice.Assertiveness) + int(ChoiceSelected)
            elif Attribute == "Neuroticism":
                SummaryChoice.Neuroticism = int(SummaryChoice.Neuroticism) + int(ChoiceSelected)
            elif Attribute == "Withdrawal":
                SummaryChoice.Withdrawal = int(SummaryChoice.Withdrawal) + int(ChoiceSelected)
            elif Attribute == "Volatility":
                SummaryChoice.Volatility = int(SummaryChoice.Volatility) + int(ChoiceSelected)
            elif Attribute == "Openess_to_Experience":
                SummaryChoice.Openess_to_Experience = int(SummaryChoice.Openess_to_Experience) + int(ChoiceSelected)
                SummaryChoice.Openness = int(SummaryChoice.Openness) + int(ChoiceSelected)
            elif Attribute == "Openness":
                SummaryChoice.Openess_to_Experience = int(SummaryChoice.Openess_to_Experience) + int(ChoiceSelected)
                SummaryChoice.Openness = int(SummaryChoice.Openness) + int(ChoiceSelected)
            elif Attribute == "Anxiety":
                SummaryChoice.Anxiety =  int(SummaryChoice.Anxiety) + int(ChoiceSelected)
            elif Attribute == "Depression":
                SummaryChoice.Depression =  int(SummaryChoice.Depression) + int(ChoiceSelected)
            elif Attribute == "Anger":
                SummaryChoice.Anger = int(SummaryChoice.Anger) + int(ChoiceSelected)
            elif Attribute == "PTSD":
                SummaryChoice.PTSD =  int(SummaryChoice.PTSD) + int(ChoiceSelected)
            elif Attribute == "IQ":
                SummaryChoice.IQ =  int(SummaryChoice.IQ) + int(ChoiceSelected)
            ProgressUpdate = Test_Progress(
                UserID=current_user.id,
                TestID=TestID,
                QuestionID=QID
            )
            db.session.add(ProgressUpdate)
            db.session.commit()
        Progress = db.session.query(Test_Progress.QuestionID).filter_by(TestID=TestID)
        QuestionList = db.session.query(Questions.Question,
                                        Assesments.QuestionID,
                                        Questions.MediaSource,
                                        Questions.MediaType,
                                        Questions.ModelID,
                                        Questions.ID, Assesments.TestID) \
            .join(Assesments, Assesments.QuestionID == Questions.ID) \
            .filter_by(TestID=TestID)\
            .filter(~Assesments.QuestionID.in_([P.QuestionID for P in Progress]))
        if QuestionList.count() == 0:
            session.clear()
            QuestionCounts = Assesments.query.filter_by(TestID=TestID).count()
            UpdatePTSD = SummaryResults.query.filter_by(TestID=TestID).filter_by(UserID=current_user.id).first()
            UpdatePTSD.PTSD = UpdatePTSD.PTSD/QuestionCounts
            UpdtaeStatus = Test_Status.query.filter_by(TestID=TestID).first()
            UpdtaeStatus.TestStatus ="Completed"
            UpdtaeStatus.DateCompleted=datetime.now()
            db.session.commit()
            session['TestID']=''
        AnswerList = db.session.query(Answer_Mapping.QuestionID,Answer_Mapping.AnswerID,Answers.AnswerDesc,Answers.Score)\
        .join(Answers,Answers.AnswerID==Answer_Mapping.AnswerID)
        return render_template('Clients/Assessment.html', QuestionList=QuestionList, AnswerList=AnswerList,
                               Progress=Progress)
    else:
        return redirect(url_for('profile'))


@app.route('/myTestResults',methods=['GET','POST'])
@login_required
def MyTestResults():
    UserProfile=''
    UserPersonality=''
    UserResults=''
    Personality = 1
    Anxiety = 1
    IQ = 1
    Depression = 1
    PTSD = 1
    AngetMmanagement = 1

    Volatility=0
    Extraversion = 0
    Agreeableness = 0
    Consientious = 0
    Compassion = 0
    Politeness = 0
    Neuroticism = 0
    Industriousness = 0
    Orderliness = 0
    Enthusiasm = 0
    Assertiveness = 0
    Withdrawal = 0
    Openess_to_Experience = 0
    Openness =0
    Intellect=0

    AvgAnxiety = 0
    AvgIQ = 0
    AvgDepression = 0
    AvgPTSD = 0
    AvgAngetMmanagement = 0

    UserID = current_user.id
    UserProfile = db.session.query(Users.GenderID,
                                   Users.img,
                                   Users.id,
                                   Users.Other_Names,
                                   Users.Sur_Name,
                                   Users.EmailAddress,
                                   Users.Nationality,
                                   Users.DoB,
                                   Users.GenderID,
                                   Gender.Gender)\
        .join(Gender, Gender.ID == Users.GenderID).filter(Users.id == UserID).first()

    print(UserProfile.GenderID)
    UserPersonality = db.session.query(Tests.Name,Tests.ID,Tests.TestType,
        Test_Status.TestStatus)\
        .join(Tests,Tests.ID==Test_Status.TestID).filter(Test_Status.UserID==UserID)

    UserResults = db.session.query(SummaryResults.TestID,
                                     SummaryResults.PTSD,
                                   SummaryResults.Extraversion,
                                   SummaryResults.Agreeableness,
                                   SummaryResults.Consientious,
                                   SummaryResults.Compassion,
                                   SummaryResults.Politeness,
                                   SummaryResults.Neuroticism,
                                   SummaryResults.Anger,
                                   SummaryResults.PTSD,
                                   SummaryResults.Anxiety,
                                   SummaryResults.Depression,
                                   SummaryResults.IQ,
                                   SummaryResults.Industriousness,
                                   SummaryResults.Orderliness,
                                   SummaryResults.Enthusiasm,
                                   SummaryResults.Assertiveness,
                                   SummaryResults.Withdrawal,
                                   SummaryResults.Volatility,
                                   SummaryResults.Intellect,
                                   SummaryResults.Openess_to_Experience,
                                   SummaryResults.Openness,
                                   SummaryResults.UID,
                                   SummaryResults.UserID,
                                     Tests.Name,
                                   Tests.TestType)\
        .join(Tests,Tests.ID==SummaryResults.TestID).filter(SummaryResults.UserID==UserID)

    #Tests_Taken = db.session.query(Tests.TestType,Tests.Name)
    for P in UserResults:
        if P.TestType == "Personality":
            Personality=Personality+1
            Extraversion = Extraversion+P.Extraversion
            Agreeableness = Agreeableness+P.Agreeableness
            Consientious = Consientious+P.Consientious
            Compassion = Compassion+P.Compassion
            Politeness = Politeness+P.Politeness
            Neuroticism = Neuroticism+P.Neuroticism
            Industriousness = Industriousness+P.Industriousness
            Orderliness = Orderliness+P.Orderliness
            Enthusiasm = Enthusiasm+P.Enthusiasm
            Assertiveness = Assertiveness+P.Assertiveness
            Openness = Openness+P.Openness
            Withdrawal = Withdrawal+P.Withdrawal
            Volatility = Volatility+P.Volatility
            Intellect = Intellect+P.Intellect
            Openess_to_Experience = Openess_to_Experience+P.Openess_to_Experience
            print(P.TestType)
        if P.TestType == "Anxiety":
            Anxiety=Anxiety+1
            AvgAnxiety=AvgAnxiety+P.Anxiety
            print(P.TestType)
        if P.TestType == "IQ":
            IQ=IQ+1
            AvgIQ=AvgIQ+P.IQ
            print(P.TestType)
        if P.TestType == "Depression":
            Depression=Depression+1
            AvgDepression=AvgDepression+P.Depression
            print(P.TestType)
        if P.TestType == "PTSD":
            PTSD=PTSD+1
            AvgPTSD=AvgPTSD+P.PTSD
            print(P.TestType)
        if P.TestType == "AngerManagement":
            AngetMmanagement=AngetMmanagement+1
            AvgAngetMmanagement=AvgAngetMmanagement+P.Anger
            print(P.TestType)
        print(Personality," -- ",Anxiety)

    if Personality>1:
        Personality=Personality-1
    if Anxiety>1:
        Anxiety=Anxiety-1
    if AvgIQ>1:
        IQ=IQ-1
    if Depression>1:
        Depression=Depression-1
    if PTSD>1:
        PTSD=PTSD-1
    if AngetMmanagement>1:
        AngetMmanagement=AngetMmanagement-1

    Extraversion = Extraversion/Personality
    Agreeableness = Agreeableness/Personality
    Consientious = Consientious/Personality
    Compassion = Compassion/Personality
    Politeness = Politeness/Personality
    Neuroticism = Neuroticism/Personality
    Industriousness = Industriousness/Personality
    Orderliness = Orderliness/Personality
    Openness = Openness/Personality
    Enthusiasm = Enthusiasm/Personality
    Assertiveness = Assertiveness/Personality
    Withdrawal = Withdrawal/Personality
    Volatility = Volatility/Personality
    Intellect = Intellect/Personality
    Openess_to_Experience = Openess_to_Experience/Personality


    AvgAnxiety = int(AvgAnxiety/Anxiety)
    AvgIQ = int(AvgIQ/IQ)
    AvgDepression = int(AvgDepression/Depression)
    AvgPTSD = int(AvgPTSD/PTSD)
    AvgAngetMmanagement = int(AvgAngetMmanagement/AngetMmanagement)
    return render_template('Clients/TestAnalysis.html',
                           AvgIQ=AvgIQ,
                           AvgDepression=AvgDepression,
                           AvgPTSD=AvgPTSD,
                           AvgAngetMmanagement=AvgAngetMmanagement,
                           AvgAnxiety=AvgAnxiety,
                           Extraversion=Extraversion / Personality,
                           Agreeableness = Agreeableness,
                           Consientious = Consientious,
                           Volatility=Volatility,
                           Compassion = Compassion,
                           Politeness = Politeness,
                           Neuroticism = Neuroticism,
                           Industriousness = Industriousness,
                           Orderliness = Orderliness,
                           Enthusiasm = Enthusiasm,
                           Assertiveness = Assertiveness,
                           Withdrawal = Withdrawal,
                           Intellect=Intellect,
                           Openness=Openness,
                           Openess_to_Experience = Openess_to_Experience,
                           UserResults=UserResults,UserProfile=UserProfile,UserPersonality=UserPersonality)