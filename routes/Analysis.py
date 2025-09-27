from datetime import datetime
import time
import re
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Integer

from src.DBConnect import *
from flask_login import login_required, current_user

from src.models.Admin import *
from src.models.Questions import *
from src.models.Results import *
from src.routes.Login import requires_roles


@app.route('/search',methods=['GET','POST'])
@login_required
@requires_roles('Admin','Assessor')
def Search():
    Genders=[]
    AgeList=[]
    Careers=[]
    Countries=[]
    GenderDistribution=0
    AgeDistribution =0
    SearchResults=0
    if request.method=='POST':
        Gender = str(re.sub('[^0-9]+', '',request.form['TXTGender']))
        Age = str(re.sub('[^0-9/]+', '',request.form['TXTAge']))
        SearchResults = Users.query.filter(Users.GenderID.like('%'+Gender+'%'))\
            .filter(Users.DoB.like('%'+Age+'%'))
        AttributesList = db.session.query(SummaryResults.TestID,SummaryResults.UserID).all()
        AttributeCount=len(AttributesList)
        for S in SearchResults:
            print(S.GenderID)
            Genders.append(S.GenderID)
            AgeList.append(S.DoB)
            #Countries.append(S.Country)
            #Careers.append(S.Career)
        GenderDistribution = SearchResults.count()
        print("Male: ", GenderDistribution," --- ",AttributeCount)
    return render_template('Admin/Analysis/Search.html',GenderDistribution=GenderDistribution)