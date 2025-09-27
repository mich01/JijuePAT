from collections import Counter
from datetime import datetime
import time
import re

from flask import render_template, request, url_for
from werkzeug.utils import secure_filename, redirect

from flask_security import UserMixin, RoleMixin
from sqlalchemy import Integer, func

from src.DBConnect import app, db
from flask_login import login_required, current_user

from src.models.Admin import Users, Roles, UserAssignment,Gender,Institutions, InstitutionLevels
from src.models.Questions import *
from src.models.Results import SummaryResults
from src.models.profile import Friends
from src.routes.Login import requires_roles



@app.route('/ViewProfile')
@login_required
@requires_roles('Admin','Assessor','User')
def EditProfile():
    UserSelected = Users.query.filter(Users.id == current_user.id).first()
    return render_template("Clients/EditProfile.html",UserSelected=UserSelected)



@app.route('/SubmitionComplete',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor','User')
def SubmitionComplete():
    if request.method=='POST':
        TestID = str(re.sub('[^0-9]+', '',request.form['TestID']))
        print("Test Completed: "+TestID)
        UpdtaeStatus = Test_Status.query.filter_by(TestID=TestID, UserID=current_user.id).first()
        print("Test Completed data: " + str(UpdtaeStatus))
        UpdtaeStatus.TestStatus = "Completed"
        UpdtaeStatus.timeCompleted=datetime.now()
        db.session.commit()
        return redirect(url_for('Home'))
    else:
        return redirect(url_for('Home'))

@app.route('/AllTests',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor','User')
def AllTests():

    return render_template("Clients/Tests.html")


@app.route('/invalidTest', methods=['GET','POST'])
@login_required
def InvalidTest():

    return render_template('/Clients/TestTaken.html')

@app.route('/takeTest', methods=['GET','POST'])
@login_required
def TakeTest():
    QuestionList =[]
    AnswerList   =[]
    ActiveTest =[]
    if request.method=='POST':
        TestID = str(re.sub('[^0-9]+', '',request.form['TestSelected']))
        CurrentStatus = Test_Status.query.filter(Test_Status.UserID==current_user.id, Test_Status.TestID==TestID).first()
        if CurrentStatus and CurrentStatus.TestStatus == "Completed":
            return redirect(url_for('InvalidTest'))
        if not CurrentStatus:
            CurrentStatus = Test_Status(
                TestID=TestID,
                UserID=current_user.id,
                TestStatus="Incomplete",
                DateStarted=datetime.now(),
                DateCompleted=datetime.now()
            )
            db.session.add(CurrentStatus)
            db.session.commit()
            SummaryChoice = SummaryResults.query.filter_by(UserID=current_user.id) \
                .filter_by(TestID=TestID).first()
            if not SummaryChoice:
                NewTest= SummaryResults(
                    TestID=TestID,
                    PTSD=0,
                    Extraversion=0,
                    Agreeableness=0,
                    Consientious=0,
                    Compassion=0,
                    Politeness=0,
                    Neuroticism=0,
                    Anger=0,
                    Anxiety=0,
                    Depression=0,
                    IQ=0,
                    Likable=0,
                    Industriousness=0,
                    Orderliness=0,
                    Enthusiasm=0,
                    Assertiveness=0,
                    Withdrawal=0,
                    Volatility=0,
                    Intellect=0,
                    Openess_to_Experience=0,
                    Openness=0,
                    UserID=current_user.id,
                    timestamp=datetime.now()
                )
                db.session.add(NewTest)
                db.session.commit()
        QuestionList = db.session.query(Questions.ID,
                                        Questions.Question,
                                        Questions.ModelID,
                                        Questions.MediaType,
                                        Questions.MediaSource,
                                        Questions.Description,
                                        Assesments.TestID)\
            .join(Assesments,Assesments.QuestionID==Questions.ID).filter(Assesments.TestID==TestID)
        AnswerList = db.session.query(Answer_Mapping.QuestionID,Answer_Mapping.AnswerID,Answers.AnswerDesc,Answers.Score)\
            .join(Answers,Answers.AnswerID==Answer_Mapping.AnswerID)
        return render_template('Clients/Assessment.html',TestID=TestID,QuestionList=QuestionList,AnswerList=AnswerList)

@app.route('/SubmitResults',methods=['GET','POST'])
@login_required
@requires_roles('User')
def SubmitResults():
    if request.method =='POST':
        ChoiceSelected = str(re.sub('[^0-9]+', '',request.form['Answer']))
        Question = str(re.sub('[^0-9]+', '',request.form['Question']))
        TestID = str(re.sub('[^0-9]+', '',request.form['TestID']))
        print("INPUTS: "+str(ChoiceSelected)+" and the question is "+str(Question)+" TestID: "+TestID)
        CurrentTest = Test_Progress.query.filter(Test_Progress.QuestionID==Question, Test_Progress.TestID==TestID).first()
        QuestionDetails = Questions.query.filter(Questions.ID==Question).first()
        NumQuestions = Assesments.query.filter(Assesments.TestID==TestID).count()
        if not CurrentTest:
            NewProgress = Test_Progress(
                QuestionID=Question,
                TestID=TestID,
                UserID=current_user.id,
                timeCompleted=datetime.now())
            db.session.add(NewProgress)
            db.session.commit()
            NewAnswer =Test_Response(
                QuestionID=Question,
                UserID=current_user.id,
                TestID=TestID,
                AnswerSelected=ChoiceSelected)
            db.session.add(NewAnswer)
            db.session.commit()
        Attribute = QuestionDetails.ModelID
        print(Attribute, " scores ", ChoiceSelected, " Question ", Question)
        if TestID != None:
            SummaryChoice = SummaryResults.query.filter_by(UserID=current_user.id) \
                .filter_by(TestID=TestID).first()
            if Attribute == "Intelect":
                SummaryChoice.Intellect = int(SummaryChoice.Intellect) + int(ChoiceSelected)
            elif Attribute == "Agreeableness":
                SummaryChoice.Agreeableness = int(SummaryChoice.Agreeableness) + int(ChoiceSelected)
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
            elif Attribute == "Openness":
                SummaryChoice.Openness = int(SummaryChoice.Openness) + int(ChoiceSelected)
            elif Attribute == "Anxiety":
                SummaryChoice.Anxiety = int(SummaryChoice.Anxiety) + ((int(ChoiceSelected)*20)/NumQuestions)
            elif Attribute == "Depression":
                SummaryChoice.Depression = int(SummaryChoice.Depression) + ((int(ChoiceSelected)*20)/NumQuestions)
            elif Attribute == "Anger":
                SummaryChoice.Anger = int(SummaryChoice.Anger) + ((int(ChoiceSelected)*20)/NumQuestions)
            elif Attribute == "PTSD":
                SummaryChoice.PTSD = int(SummaryChoice.PTSD) + ((int(ChoiceSelected)*20)/NumQuestions)
                print(str(SummaryChoice.PTSD) + " -- " + str(NumQuestions) + " ----+----- " + str(SummaryChoice.PTSD))
            elif Attribute == "IQ":
                SummaryChoice.IQ = int(SummaryChoice.IQ) + ((int(ChoiceSelected)*20)/NumQuestions)
            db.session.commit()
    return "Done"

@app.route('/MyTests',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor','User')
def MyTests():
    UserProfile = ''
    UserPersonality = ''
    UserResults = ''
    Personality = 1
    Anxiety = 1
    IQ = 1
    Depression = 1
    PTSD = 1
    AngetMmanagement = 1

    Volatility = 0
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
    Openness = 0
    Intellect = 0

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
                                   Gender.Gender) \
        .join(Gender, Gender.ID == Users.GenderID).filter(Users.id == UserID).first()

    print(UserProfile.GenderID)
    UserPersonality = db.session.query(Tests.Name, Tests.ID, Tests.TestType,
                                       Test_Status.TestStatus) \
        .join(Tests, Tests.ID == Test_Status.TestID).filter(Test_Status.UserID == UserID)

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
                                   Tests.TestType) \
        .join(Tests, Tests.ID == SummaryResults.TestID).filter(SummaryResults.UserID == UserID)
    # Tests_Taken = db.session.query(Tests.TestType,Tests.Name)
    for P in UserResults:
        if P.TestType == "Personality":
            Personality = Personality + 1
            Extraversion = Extraversion + P.Extraversion
            Agreeableness = Agreeableness + P.Agreeableness
            Consientious = Consientious + P.Consientious
            Compassion = Compassion + P.Compassion
            Politeness = Politeness + P.Politeness
            Neuroticism = Neuroticism + P.Neuroticism
            Industriousness = Industriousness + P.Industriousness
            Orderliness = Orderliness + P.Orderliness
            Enthusiasm = Enthusiasm + P.Enthusiasm
            Assertiveness = Assertiveness + P.Assertiveness
            Openness = Openness + P.Openness
            Withdrawal = Withdrawal + P.Withdrawal
            Volatility = Volatility + P.Volatility
            Intellect = Intellect + P.Intellect
            Openess_to_Experience = Openess_to_Experience + P.Openess_to_Experience
            print(P.TestType)
        if P.TestType == "Anxiety":
            Anxiety = Anxiety + 1
            AvgAnxiety = AvgAnxiety + P.Anxiety
            print(P.TestType)
        if P.TestType == "IQ":
            IQ = IQ + 1
            AvgIQ = AvgIQ + P.IQ
            print(P.TestType)
        if P.TestType == "Depression":
            Depression = Depression + 1
            AvgDepression = AvgDepression + P.Depression
            print(P.TestType)
        if P.TestType == "PTSD":
            PTSD = PTSD + 1
            AvgPTSD = AvgPTSD + P.PTSD
            print(P.TestType)
        if P.TestType == "AngerManagement":
            AngetMmanagement = AngetMmanagement + 1
            AvgAngetMmanagement = AvgAngetMmanagement + P.Anger
            print(P.TestType)
        print(Personality, " -- ", Anxiety)

    if Personality > 1:
        Personality = Personality - 1
    if Anxiety > 1:
        Anxiety = Anxiety - 1
    if AvgIQ > 1:
        IQ = IQ - 1
    if Depression > 1:
        Depression = Depression - 1
    if PTSD > 1:
        PTSD = PTSD - 1
    if AngetMmanagement > 1:
        AngetMmanagement = AngetMmanagement - 1

    Extraversion = Extraversion / Personality
    Agreeableness = Agreeableness / Personality
    Consientious = Consientious / Personality
    Compassion = Compassion / Personality
    Politeness = Politeness / Personality
    Neuroticism = Neuroticism / Personality
    Industriousness = Industriousness / Personality
    Orderliness = Orderliness / Personality
    Openness = Openness / Personality
    Enthusiasm = Enthusiasm / Personality
    Assertiveness = Assertiveness / Personality
    Withdrawal = Withdrawal / Personality
    Volatility = Volatility / Personality
    Intellect = Intellect / Personality
    Openess_to_Experience = Openess_to_Experience / Personality

    AvgAnxiety = int(AvgAnxiety / Anxiety)
    AvgIQ = int(AvgIQ / IQ)
    AvgDepression = int(AvgDepression / Depression)
    AvgPTSD = int(AvgPTSD / PTSD)
    AvgAngetMmanagement = int(AvgAngetMmanagement / AngetMmanagement)
    return render_template('Clients/TestAnalysis.html',
                           AvgIQ=AvgIQ,
                           AvgDepression=AvgDepression,
                           AvgPTSD=AvgPTSD,
                           AvgAngetMmanagement=AvgAngetMmanagement,
                           AvgAnxiety=AvgAnxiety,
                           Extraversion=Extraversion / Personality,
                           Agreeableness=Agreeableness,
                           Consientious=Consientious,
                           Volatility=Volatility,
                           Compassion=Compassion,
                           Politeness=Politeness,
                           Neuroticism=Neuroticism,
                           Industriousness=Industriousness,
                           Orderliness=Orderliness,
                           Enthusiasm=Enthusiasm,
                           Assertiveness=Assertiveness,
                           Withdrawal=Withdrawal,
                           Intellect=Intellect,
                           Openness=Openness,
                           Openess_to_Experience=Openess_to_Experience,
                           UserResults=UserResults, UserProfile=UserProfile,
                           UserPersonality=UserPersonality)
