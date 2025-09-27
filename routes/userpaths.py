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
from src.models.profile import Friends

Status =''

@app.route('/home')
@login_required
def Home():
    Test_List = db.session.query(Tests.ID,Tests.Name,Tests.Status, Tests.Description, Tests.TestType, Test_Assignments.UserID)\
        .join(Test_Assignments,Test_Assignments.TestID==Tests.ID).filter(Test_Assignments.UserID==current_user.id    )
    My_Tests = db.session.query(Tests.Name, Tests.ID, Test_Status.TestStatus, Test_Assignments.UserID) \
        .join(Test_Status, Test_Status.TestID == Tests.ID).filter(Test_Status.TestStatus == "Completed")
    Summary = []
    FriendsList = Friends.query.filter_by(ToID=current_user.id)
    Following = Friends.query.filter_by(FromID=current_user.id)
    Following_Count = Following.count()
    FollowerCount = FriendsList.count()
    ComprehensiveResults = []
    if request.method == 'POST':
        Test_Taken = str(re.sub('[^0-9]+', '',request.form['TestTaken']))
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
            .outerjoin(Tests, Tests.ID == SummaryResults.TestID).filter(SummaryResults.TestID == Test_Taken).first()

        ComprehensiveResults = db.session.query(SummaryResults.timestamp,
                                                SummaryResults.UserID,
                                                SummaryResults.Neuroticism,
                                                SummaryResults.Extraversion,
                                                SummaryResults.Agreeableness,
                                                SummaryResults.TestID,
                                                SummaryResults.ID,
                                                SummaryResults.Compassion,
                                                SummaryResults.Conscientiousness,
                                                SummaryResults.Assertiveness,
                                                SummaryResults.Enthusiasm,
                                                SummaryResults.Industriousness,
                                                SummaryResults.Intellect,
                                                SummaryResults.Openness,
                                                SummaryResults.Openness_to_Experience,
                                                SummaryResults.Orderliness,
                                                SummaryResults.Politeness,
                                                SummaryResults.Volatility,
                                                SummaryResults.Withdrawal) \
            .outerjoin(Users, Users.id == SummaryResults.TestID) \
            .outerjoin(Tests, Tests.ID == SummaryResults.TestID).filter(SummaryResults.TestID == Test_Taken).first()
    return render_template('Clients/Home.html', My_Tests=My_Tests, Test_List=Test_List, Summary=Summary,
                           ComprehensiveResults=ComprehensiveResults,
                           FriendsList=FriendsList, FollowerCount=FollowerCount,
                           Following_Count=Following_Count,
                           Following=Following)
