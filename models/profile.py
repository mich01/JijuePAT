from src.DBConnect import db
from flask_login import UserMixin
class JsonModel(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Friends(UserMixin, db.Model):
    __tablename__ = 'tbl_network'
    UID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FromID = db.Column(db.Integer, nullable=False)
    ToID = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self,FromID,ToID):
        self.FromID = FromID
        self.ToID = ToID
