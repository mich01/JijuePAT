from src.DBConnect import db
from flask_login import UserMixin
class JsonModel(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class Questions(UserMixin, db.Model):
    __tablename__ = 'tbl_Questions'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MediaType = db.Column(db.String(6), nullable=False)
    Question = db.Column(db.String(500), unique=True, nullable=False)
    MediaSource = db.Column(db.String(500))
    Description = db.Column(db.String(500), nullable=False)
    ModelID = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self,Question, Description,ModelID,MediaType,MediaSource,timestamp):
        self.Question =Question
        self.ModelID = ModelID
        self.Description =Description
        self.MediaType = MediaType
        self.MediaSource = MediaSource
        self.timestamp = timestamp


class Answers(UserMixin, db.Model):
    __tablename__ = 'tbl_AnswerOptions'
    AnswerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AnswerDesc = db.Column(db.String(500), unique=True, nullable=False)
    Score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, AnswerDesc,Score,timestamp):
        self.AnswerDesc = AnswerDesc
        self.Score =Score
        self.timestamp = timestamp

class Tests(UserMixin, db.Model):
    __tablename__ = 'tbl_Tests'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Creator = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String(20), nullable=False)
    Status = db.Column(db.String(7), nullable=False)
    Description = db.Column(db.String(100), nullable=False)
    TestType = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self,Name,Creator, TestType,Status,Description,timestamp):
        self.Name = Name
        self.Creator = Creator
        self.Status = Status
        self.Description = Description
        self.TestType =TestType
        self.timestamp = timestamp

class Assesments(UserMixin, db.Model):
    __tablename__ = 'tbl_Assessment'
    UID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TestID = db.Column(db.Integer, nullable=False)
    QuestionID = db.Column(db.Integer, nullable=False)
    UserAdding = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self,TestID,QuestionID,UserAdding, timestamp):
        self.TestID = TestID
        self.QuestionID = QuestionID
        self.UserAdding = UserAdding
        self.timestamp = timestamp


class Test_Status(UserMixin, db.Model):
    __tablename__ = 'tbl_TestStatus'
    UID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TestID = db.Column(db.Integer, nullable=False)
    UserID = db.Column(db.Integer, nullable=False)
    TestStatus = db.Column(db.String(10), nullable=False)
    DateStarted = db.Column(db.DateTime, nullable=False)
    DateCompleted = db.Column(db.DateTime, nullable=True)

    def __init__(self,TestID,UserID,TestStatus,DateStarted,DateCompleted):
        self.TestID = TestID
        self.UserID = UserID
        self.TestStatus = TestStatus
        self.DateStarted = DateStarted
        self.DateCompleted = DateCompleted

class Test_Progress(UserMixin, db.Model):
    __tablename__ = 'tbl_userTests'
    UID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TestID = db.Column(db.Integer, nullable=False)
    UserID = db.Column(db.Integer, nullable=False)
    QuestionID = db.Column(db.Integer, nullable=False)
    timeCompleted = db.Column(db.DateTime, nullable=True)

    def __init__(self,TestID,UserID,QuestionID,timeCompleted):
        self.TestID = TestID
        self.UserID = UserID
        self.QuestionID = QuestionID
        self.timeCompleted=timeCompleted

class Answer_Mapping(UserMixin, db.Model):
    __tablename__ = 'tbl_AnswerMapping'
    UID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    QuestionID = db.Column(db.Integer, nullable=False)
    AnswerID = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self,QuestionID,AnswerID,timestamp):
        self.QuestionID = QuestionID
        self.AnswerID = AnswerID
        self.timestamp =timestamp

class Test_Assignments(UserMixin, db.Model):
    __tablename__ = 'tbl_Accessible_tests'
    UID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, nullable=False)
    TestID = db.Column(db.Integer, nullable=False)
    AdminID = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=True)

    def __init__(self,UserID,TestID,AdminID,timestamp):
        self.UserID = UserID
        self.TestID = TestID
        self.AdminID = AdminID
        self.timestamp = timestamp

class Test_Response(UserMixin, db.Model):
    __tablename__ = 'tbl_TestResponse'
    UID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, nullable=False)
    TestID = db.Column(db.Integer, nullable=False)
    QuestionID = db.Column(db.Integer, nullable=False)
    AnswerSelected = db.Column(db.Integer, nullable=False)

    def __init__(self, UserID, TestID, QuestionID, AnswerSelected):
        self.UserID = UserID
        self.TestID = TestID
        self.QuestionID = QuestionID
        self.AnswerSelected = AnswerSelected




