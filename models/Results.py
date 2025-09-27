#tbl_Summary

from src.DBConnect import db
from flask_login import UserMixin
class JsonModel(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SummaryResults(UserMixin, db.Model):
    __tablename__ = 'tbl_Summary'
    UID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, nullable=False)
    TestID = db.Column(db.Integer, nullable=False)
    Agreeableness = db.Column(db.Integer, nullable=True)
    Compassion = db.Column(db.Integer, nullable=True)
    Politeness = db.Column(db.Integer, nullable=True)
    Consientious = db.Column(db.Integer, nullable=True)
    Orderliness = db.Column(db.Integer, nullable=True)
    Industriousness = db.Column(db.Integer, nullable=True)
    Extraversion = db.Column(db.Integer, nullable=True)
    Enthusiasm = db.Column(db.Integer, nullable=True)
    Assertiveness = db.Column(db.Integer, nullable=True)
    Neuroticism = db.Column(db.Integer, nullable=True)
    Withdrawal = db.Column(db.Integer, nullable=True)
    Volatility = db.Column(db.Integer, nullable=True)
    Openess_to_Experience = db.Column(db.Integer, nullable=True)
    Intellect = db.Column(db.Integer, nullable=True)
    Openness = db.Column(db.Integer, nullable=True)
    Anxiety = db.Column(db.Integer, nullable=True)
    Anger = db.Column(db.Integer, nullable=True)
    IQ = db.Column(db.Integer, nullable=True)
    Likable = db.Column(db.Integer, nullable=True)
    PTSD = db.Column(db.Integer, nullable=True)
    Depression = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self,PTSD,IQ,Depression,Anger,Likable,UserID,TestID,Agreeableness,Compassion,Politeness,Consientious,Orderliness,Industriousness,
    Extraversion,Enthusiasm,Anxiety,Assertiveness,Neuroticism,Withdrawal,Volatility,Openess_to_Experience,Intellect,Openness,timestamp):
        self.TestID = TestID
        self.UserID = UserID
        self.Agreeableness = Agreeableness
        self.Compassion = Compassion
        self.Politeness = Politeness
        self.Orderliness = Orderliness
        self.Consientious = Consientious
        self.Industriousness = Industriousness
        self.Extraversion = Extraversion
        self.Enthusiasm = Enthusiasm
        self.Assertiveness = Assertiveness
        self.Neuroticism = Neuroticism
        self.Withdrawal = Withdrawal
        self.Volatility = Volatility
        self.Openess_to_Experience = Openess_to_Experience
        self.Intellect = Intellect
        self.Openness = Openness
        self.Anxiety = Anxiety
        self.Anger=Anger
        self.IQ=IQ
        self.PTSD = PTSD
        self.Depression=Depression
        self.Likable =Likable
        self.timestamp = timestamp
