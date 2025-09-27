from src.DBConnect import db
from flask_login import UserMixin
class JsonModel(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}





class Users(UserMixin, db.Model):
    __tablename__ = 'tbl_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EmailAddress = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(200))
    UserName = db.Column(db.String(100), unique=True, nullable=False)
    Pass_word = db.Column(db.String(500), nullable=False)
    Sur_Name = db.Column(db.String(100), nullable=False)
    Other_Names = db.Column(db.String(100), nullable=False)
    Nationality = db.Column(db.String(50), nullable=False)
    GenderID = db.Column(db.Integer, nullable=False)
    Role_ID = db.Column(db.Integer, nullable=False)
    User_Status = db.Column(db.Integer, nullable=False)
    Date_Created = db.Column(db.DateTime,nullable=True)
    DoB = db.Column(db.Date,nullable =True)

    def __init__(self, DoB,img,Nationality,User_Status, EmailAddress,UserName, Pass_word, Sur_Name,Other_Names,GenderID,Role_ID,Date_Created):
        self.EmailAddress =EmailAddress
        self.UserName = UserName
        self.Pass_word = Pass_word
        self.img = img
        self.DoB=DoB
        self.Sur_Name = Sur_Name
        self.Other_Names = Other_Names
        self.GenderID = GenderID
        self.Role_ID = Role_ID
        self.User_Status =User_Status
        self.Nationality=Nationality
        self.Date_Created=Date_Created

        #roles = db.relationships('Role',secondary='user_roles',backref=db.backref('Users',lazy='dynamic'))

class Roles(UserMixin, db.Model):
    __tablename__ = 'tbl_Roles'
    Role_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Role_type = db.Column(db.String(200), nullable=False)
    Description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime,nullable=False)

    def __init__(self,Role_ID, Role_type,Description):
        self.Role_ID =Role_ID
        self.Role_type = Role_type
        self.Description = Description


class User_Status(UserMixin, db.Model):
    __tablename__ = 'tbl_Status'
    Status_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Status_type = db.Column(db.String(200), nullable=False)
    Description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime,nullable=False)

    def __init__(self,Status_ID, Status_type,Description):
        self.Status_ID =Status_ID
        self.Status_type = Status_type
        self.Description = Description

class Gender(UserMixin, db.Model):
    __tablename__ = 'tbl_Gender'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Gender = db.Column(db.String(200), nullable=False)

    def __init__(self,ID, Gender):
        self.ID =ID
        self.Gender = Gender


class Institutions(UserMixin, db.Model):
    __tablename__ = 'tbl_Institutions'
    InstitutionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    InstitutionName = db.Column(db.String(200), nullable=False)
    InstitutionAddress = db.Column(db.String(200), nullable=False)
    GeoMap = db.Column(db.String(200), nullable=False)
    InstitutionLevel = db.Column(db.String(200), nullable=False)
    AuthorityID = db.Column(db.String(200), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, InstitutionName,InstitutionAddress,GeoMap,InstitutionLevel,AuthorityID):
        self.InstitutionName = InstitutionName
        self.InstitutionAddress=InstitutionAddress
        self.GeoMap=GeoMap
        self.InstitutionLevel = InstitutionLevel
        self.AuthorityID=AuthorityID

class InstitutionLevels(UserMixin, db.Model):
    __tablename__ = 'tbl_Institution_Levels'
    LevelID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    LevelType = db.Column(db.String(200), nullable=False)
    Description = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, LevelType,Description):
        self.LevelType = LevelType
        self.Description=Description

class UserAssignment(UserMixin, db.Model):
    __tablename__ = 'tbl_Assessors'
    UID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer,nullable=False)
    AssessorID = db.Column(db.Integer, nullable=False)
    AssignerID = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime,nullable=False)

    def __init__(self,UserID, AssessorID,AssignerID,timestamp):
        self.UserID =UserID
        self.AssessorID = AssessorID
        self.AssignerID = AssignerID
        self.timestamp = timestamp
