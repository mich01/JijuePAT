from sqlalchemy import Integer
import re
from src.DBConnect import *
from flask_login import login_required, current_user
from datetime import datetime
from src.models.Admin import *
from src.models.Questions import *
from src.models.Results import  SummaryResults
from src.models.profile import Friends
from src.routes.Login import requires_roles

Status=''

@app.route('/Questions/')
@login_required
@requires_roles('Admin','Assessor')
def QuestionsModule():
    QuestionList = Questions.query.all()
    AnswerList = db.session.query(Answer_Mapping.QuestionID,Answer_Mapping.UID,Answer_Mapping.AnswerID,Answers.AnswerDesc)\
        .outerjoin(Answers,Answers.AnswerID==Answer_Mapping.AnswerID)
    All_Answers = Answers.query.all()
    return render_template('Admin/Questions.html',QuestionList=QuestionList,AnswerList=AnswerList,All_Answers=All_Answers,Status=Status)

@app.route('/Answers')
@login_required
@requires_roles('Admin','Assessor')
def AnswersModule():
    QuestionList = Questions.query.all()
    AnswerList = Answers.query.all()
    return render_template('Admin/Answers.html',QuestionList=QuestionList,AnswerList=AnswerList,Status=Status)



@app.route('/Tests',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def TestsModule():
    Test_List=[]
    Questions_List=[]
    AssignedQuestions=''
    if request.method == 'POST':
        Status = str(re.sub('[^0-9]+', '',request.form['Status']))
        TestName = str(re.sub('[^A-Za-z0-9]+ ', '',request.form['Name']))
        TestType = str(re.sub('[^A-Za-z0-9]+.', '',request.form['TestType']))
        Creator = str(re.sub('[^0-9]+', '',request.form['Creator']))
        Description = str(re.sub('[^A-Za-z0-9]+ ', '',request.form['Description']))
        Test_List =db.session.query(Tests.ID,Tests.TestType,Tests.Name,Tests.timestamp,Tests.Description,Tests.Status,Tests.Creator,Users.UserName)\
            .join(Users, Users.id==Tests.Creator).filter(Tests.Status.ilike('%'+Status+'%'))\
            .filter(Tests.Name.ilike('%'+TestName+'%'))\
            .filter(Tests.Description.ilike('%'+Description+'%'))\
            .filter(Tests.TestType.ilike('%'+TestType+'%'))\
            .filter(Users.UserName.ilike('%'+Creator+'%'))
        Questions_List = Questions.query.all()
        AssignedQuestions = db.session.query(Assesments.TestID,Assesments.UID,Assesments.QuestionID,Questions.ID,Questions.Question)\
            .join(Questions,Questions.ID==Assesments.QuestionID)
        flash("Test Added")
    return render_template('Admin/Tests.html',Test_List=Test_List, Questions_List=Questions_List,AssignedQuestions=AssignedQuestions)

@app.route('/AddQuestions',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def addQuestions():
    if request.method=='POST':
        Question = str(re.sub('[^A-Za-z0-9]+ ', '',request.form['Question']))
        QuestionType = str(re.sub('[^A-Za-z]+', '',request.form['MediaType']))
        Source = request.form['MediaLink']
        Description = request.form['Description']
        Model = str(re.sub('[^A-Za-z]+', '',request.form['Model']))
        if not Source:
            Source="0";
        QuestionValues = Questions(
            Question=Question,
            ModelID=Model,
            Description=Description,
            MediaType=QuestionType,
            MediaSource=Source,
            timestamp=datetime.now()
        )
        db.session.add(QuestionValues)
        db.session.commit()
        flash("Question Successfully Added")
    return redirect(url_for('QuestionsModule',Status=Status))

@app.route('/EditQuestions',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def editQuestions():
    if request.method=='POST':
        QID = str(re.sub('[^0-9]+', '',request.form['QuestionID']))
        Question = str(re.sub('[^A-Za-z0-9]+ ', '',request.form['Question']))
        QuestionType = str(re.sub('[^A-Za-z]+', '',request.form['MediaType']))
        Source = request.form['MediaLink']
        Description = request.form['Description']
        Model = str(re.sub('[^A-Za-z]+', '',request.form['Model']))
        EditableQuestion = Questions.query.filter_by(ID=QID).first()
        EditableQuestion.Question=Question
        EditableQuestion.ModelID=Model
        EditableQuestion.Description=Description
        EditableQuestion.MediaType=QuestionType
        EditableQuestion.MediaSoure=Source
        db.session.commit()
        flash("Question Updated Successfully")
    return redirect(url_for('QuestionsModule'))

@app.route('/EditAnswer',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def editAnswer():
    if request.method=='POST':
        AID = str(re.sub('[^0-9]+', '',request.form['AnswerID']))
        Answer = str(re.sub('[^A-Za-z0-9]+', '',request.form['Answer']))
        Score = str(re.sub('[^0-9]+', '',request.form['Score']))
        EditableAnswer = Answers.query.filter_by(AnswerID=AID).first()
        EditableAnswer.AnswerDesc = Answer
        EditableAnswer.Score = Score
        db.session.commit()
        flash("Answer Edited Successfully")
    return redirect(url_for('AnswersModule'))

@app.route('/DeleteQuestion',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def DeleteQuestion():
    if request.method == 'POST':
        QID = str(re.sub('[^0-9]+', '',request.form['QuestionID']))
        QuestionDeleted = Questions.query.filter_by(ID=QID).first()
        db.session.delete(QuestionDeleted)
        db.session.commit()
        flash("Question Deleted")
    return redirect(url_for('QuestionsModule'))

@app.route('/DeleteAnswer',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def DeleteAnswer():
    if request.method == 'POST':
        AID = str(re.sub('[^0-9]+', '',request.form['AnswerID']))
        AnswerDeleted = Answers.query.filter_by(AnswerID=AID).first()
        db.session.delete(AnswerDeleted)
        db.session.commit()
        flash("Answer Deleted")
    return redirect(url_for('AnswersModule'))

@app.route('/AddAnswers',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def addAnswer():
    if request.method=='POST':
        Answer = str(re.sub('[^A-Za-z0-9]+ ', '',request.form['Answer']))
        Score = str(re.sub('[^0-9]+', '',request.form['Score']))
        AnswerValues = Answers(
            AnswerDesc=Answer,
            Score=Score,
            timestamp=datetime.now(),
        )
        db.session.add(AnswerValues)
        db.session.commit()
        flash("Answer Added Successfully");
    return redirect(url_for('AnswersModule'))

@app.route('/CreateTest',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def createTest():
    if request.method=='POST':
        Name = str(re.sub('[^A-Za-z0-9]+ ', '',request.form['Name']))
        State = str(re.sub('[^A-Za-z]+', '',request.form['Status']))
        Desc = str(re.sub('[^A-Za-z0-9]+ ', '',request.form['Description']))
        TestType= str(re.sub('[^A-Za-z]+.', '',request.form['TestType']))
        CreatedTest = Tests(
            Creator = current_user.id,
            Name = Name,
            Status = State,
            TestType=TestType,
            timestamp=datetime.now(),
            Description=Desc)
        db.session.add(CreatedTest)
        db.session.commit()
        TestIDAdded =Tests.query.filter_by(Name=Name).first()
        AssignTest = Test_Assignments(
            AdminID=current_user.id,
            UserID= current_user.id,
            TestID= TestIDAdded.ID,
            timestamp=datetime.now(),
        )
        db.session.add(AssignTest)
        db.session.commit()
        flash("Test created Successfully")
    return redirect(url_for('TestsModule'))

@app.route('/EditTests',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def editTests():
    if request.method=='POST':
        TID = str(re.sub('[^0-9]+', '',request.form['ID']))
        Name = str(re.sub('[^A-Za-z0-9]+', '',request.form['Name']))
        State = str(re.sub('[^A-Za-z]+', '',request.form['Status']))
        Desc = request.form['Description']
        TestType = str(re.sub('[^A-Za-z]+', '',request.form['TestType']))
        EditableTest = Tests.query.filter_by(ID=TID).first()
        EditableTest.Name = Name
        EditableTest.Status = State
        EditableTest.Description = Desc
        EditableTest.TestType=TestType
        db.session.commit()
        flash("Test Updated Successfully")
    return redirect(url_for('TestsModule'))

@app.route('/DeleteTest',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def DeleteTest():
    if request.method == 'POST':
        AID = str(re.sub('[^0-9]+', '',request.form['ID']))
        TestDeleted = Tests.query.filter_by(ID=AID).first()
        db.session.delete(TestDeleted)
        db.session.commit()
        flash("Test Deleted")
        TestDetached = Test_Assignments.query.filter_by(TestID=AID).first()
        db.session.delete(TestDetached)
        db.session.commit()
    return redirect(url_for('TestsModule'))

@app.route('/MapQuestions',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def MapQuestions():
    if request.method == 'POST':
        QuestionsSelected = request.form.getlist('QuestionsSelected')
        TestID = str(re.sub('[^0-9]+', '',request.form['TID']))
        for Q in QuestionsSelected:
            QuestionExist = Assesments.query.filter(Assesments.QuestionID==Q,Assesments.TestID==TestID).first()
            if not QuestionExist:
                Assesment = Assesments(
                UserAdding = current_user.id,
                    TestID = TestID,
                    timestamp=datetime.now(),
                    QuestionID = Q)
                db.session.add(Assesment)
                db.session.commit()
        db.session.close()
        flash("Questions Mapped to test successfully")
    return redirect(url_for('TestsModule'))

@app.route('/MapAnswers',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def MapAnswers():
    if request.method == 'POST':
        AnswersSelected = request.form.getlist('AnswerSelected')
        QuestionID = str(re.sub('[^0-9]+', '',request.form['QID']))
        for Q in AnswersSelected:
            AnswerExist = Answer_Mapping.query.filter(Answer_Mapping.AnswerID==Q,Answer_Mapping.QuestionID==QuestionID).first()
            if not AnswerExist:
                AnswersMap = Answer_Mapping(
                QuestionID = QuestionID,
                AnswerID = Q,
                timestamp=datetime.now())
                db.session.add(AnswersMap)
                db.session.commit()
        flash("Answers Mapped to Question successfully")
    return redirect(url_for('QuestionsModule'))

@app.route('/UnMapQuestions',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def UnMapQuestions():
    if request.method == 'POST':
        QuestionsSelected = request.form.getlist('QuestionsSelected')
        for Q in QuestionsSelected:
            RemovedQuestions = Assesments.query.filter_by(UID=Q).first()
            db.session.delete(RemovedQuestions)
            db.session.commit()
        flash("Questions UNMapped to Test successfully")
    return redirect(url_for('QuestionsModule'))\


@app.route('/UnMapAnswers',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def UnMapAnswers():
    if request.method == 'POST':
        AnswersSelected = request.form.getlist('AnswerSelected')
        for A in AnswersSelected:
            UnmappedAnswers = Answer_Mapping.query.filter_by(UID=A).first()
            db.session.delete(UnmappedAnswers)
            db.session.commit()
        flash("Answers UNMapped to Question successfully")
    return redirect(url_for('QuestionsModule'))


@app.route('/Profile',methods=['GET','POST'])
@login_required
def profile():
    Test_List = Tests.query.all()
    My_Tests = db.session.query(Tests.Name,Tests.ID,Test_Status.TestStatus)\
        .join(Test_Status, Test_Status.TestID == Tests.ID).filter(Test_Status.TestStatus=="Completed")
    Summary=[]
    FriendsList = Friends.query.filter_by(ToID=current_user.id)
    Following = Friends.query.filter_by(FromID=current_user.id)
    Following_Count=Following.count()
    FollowerCount = FriendsList.count()
    ComprehensiveResults=[]
    if request.method =='POST':
        Test_Taken =request.form['TestTaken']
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
                                   Tests.Name) \
            .outerjoin(Users, Users.id == SummaryResults.TestID) \
            .outerjoin(Tests, Tests.ID == SummaryResults.TestID).filter(SummaryResults.TestID==Test_Taken).first()

        ComprehensiveResults = db.session.query(DetailedResults.timestamp,
                                                DetailedResults.UserID,
                                                DetailedResults.Neuroticism,
                                                DetailedResults.Extraversion,
                                                DetailedResults.Agreeableness,
                                                DetailedResults.TestID,
                                                DetailedResults.ID,
                                                DetailedResults.Compassion,
                                                DetailedResults.Conscientiousness,
                                                DetailedResults.Assertiveness,
                                                DetailedResults.Enthusiasm,
                                                DetailedResults.Industriousness,
                                                DetailedResults.Intellect,
                                                DetailedResults.Openness,
                                                DetailedResults.Openness_to_Experience,
                                                DetailedResults.Orderliness,
                                                DetailedResults.Politeness,
                                                DetailedResults.Volatility,
                                                DetailedResults.Withdrawal) \
            .outerjoin(Users, Users.id == DetailedResults.TestID) \
            .outerjoin(Tests, Tests.ID == DetailedResults.TestID).filter(DetailedResults.TestID==Test_Taken).first()
    return render_template('Clients/Profile.html',My_Tests=My_Tests,Test_List=Test_List, Summary=Summary,ComprehensiveResults=ComprehensiveResults,
                           FriendsList=FriendsList,FollowerCount=FollowerCount,
                           Following_Count=Following_Count,
                           Following=Following)