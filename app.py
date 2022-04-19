from utils import *
import random
from flask import Flask, render_template, escape, request, redirect
import pandas as pd
import numpy as np
import csv
import math
from sklearn import neighbors, datasets
from numpy.random import permutation
from sklearn.metrics import precision_recall_fscore_support
import UnderGraduateServer

###################### Import Blueprints ######################
from views.projects.views import projects_
from views.authentication.views import authentication_
from views.settings.views import settings_
from views.friends.views import friends_
from views.jobsandinternships.views import jobsandinternships_
###############################################################

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PERMANENT_SESSION_LIFETIME"] =  timedelta(minutes=10)
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

global COOKIE_TIME_OUT
COOKIE_TIME_OUT = 60*5

###################### Register Blueprints ######################
app.register_blueprint(projects_)
app.register_blueprint(authentication_)
app.register_blueprint(settings_)
app.register_blueprint(friends_)
app.register_blueprint(jobsandinternships_)
#################################################################

db.init_app(app)
login.init_app(app)
login.login_view = "authentication.login"

@app.before_first_request
def create_all():
    db.create_all()

@app.errorhandler(404)
def page_not_found_(e):
    return render_template("error/404.html"), 404

@app.errorhandler(405)
def page_not_foun_(e):
    return render_template("error/404.html"), 405

@app.route("/", methods = ["GET", "POST"])
@login_required
def index():
    user = UserModel.query.filter_by(name = session["username"]).first()
    data = {
        "username": session["username"],
        "user": user
    }
    return render_template("index.html",  data = data)

@app.route("/user-profile/<id>", methods = ["GET"])
@login_required
def user_profile(id):
    user = UserModel.query.filter_by(name = id).first()
    projects = ProjectsModel.query.filter_by(user_name = id)
    friend1 = FriendModel.query.filter_by(user1 = id, status = 1).all()
    friend2 = FriendModel.query.filter_by(user2 = id, status = 1).all()
    all_users = UserModel.query.all()
    data = {
        "projects": projects,
        "my_id": session["id"],
        "user": user,
        "all_users": all_users,
        "friend1": friend1,
        "friend2": friend2,
        "my_name": session["username"]
    }
    return render_template("user-profile.html", data=data)

@app.route('/graduate')
def graduate():
    return render_template('graduate.html')

@app.route('/undergraduate')
def undergraduate():
    return render_template('undergraduate.html')

def euclidean_dist(test, train, length):
    distance = 0
    for x in range(length):
        distance += np.square(test[x] - train[x])
    return np.sqrt(distance)


def knn(trainSet, test_instance, k):
 
    distances = {}
    sort = {}
    length = test_instance.shape[1]

    for x in range(len(trainSet)):
 
        distance = euclidean_dist(test_instance, trainSet.iloc[x], length)
        distances[x] = distance[0]

    sorted_distances = sorted(distances.items(), key=lambda x: x[1])
    print(sorted_distances[:5])

 
    neighbors_list = []

    for x in range(k):
        neighbors_list.append(sorted_distances[x][0])

    duplicateNeighbors = {}

    for x in range(len(neighbors_list)):
        responses = trainSet.iloc[neighbors_list[x]][-1]
        
        if responses in duplicateNeighbors:
            duplicateNeighbors[responses] += 1
        else:
            duplicateNeighbors[responses] = 1
    print(responses)

    sortedNeighbors = sorted(duplicateNeighbors.items(), key=lambda x: x[1], reverse=True)
    return(sortedNeighbors, neighbors_list)

@app.route('/undergraduatealgo')
def undergraduatealgo():
    result = UnderGraduateServer.main()
    list1 = []
    list2 = []
    for i in result:
        list1.append(i[0])
    for i in result:
        list2.append(i[1])
    return '''
        <html>
            <head>
                <title>Top-5 Undergraduate Recomended Universities</title>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">
                <link href="http://getbootstrap.com/examples/jumbotron-narrow/jumbotron-narrow.css" rel="stylesheet">
 
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous" />

                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
            </head>
            <body>
                <div class="container">     
                        <h2 style="text-align: center">Top-5 Undergraduate Recomended Universities</h2>
                        <br>
                        <p class="lead"></p>
                          <p>The Top-5 Undergraduate Recommended Universities based on your SAT Score & Maximum Tution Fees are </p>
                          <br>
                            <table class="table table-striped">
                            <tr><td><h4>S.No</h4></td><td><h4>University</h4></td><td><h4>Acceptance Rate</h4></td></tr>
                            <tr><td><p>1. </p></td><td>{result10}</td><td>{result11}</td></tr>
                            <tr><td><p>2. </p></td><td>{result20}</td><td>{result21}</td></tr>
                            <tr><td><p>3. </p></td><td>{result30}</td><td>{result31}</td></tr>
                            <tr><td><p>4. </p></td><td>{result40}</td><td>{result41}</td></tr>
                            <tr><td><p>5. </p></td><td>{result50}</td><td>{result51}</td></tr>
                            </table>
                    
     

                    <p align="center">
                    <a class="btn btn-primary" href="/" role="button">Home</a>
                    <p>
                    
                </div>
            </body>
        </html>
            '''.format(result10 = list1[0], result11 = list2[0], result20 = list1[1], result21 = list2[1],result30 = list1[2],result31 = list2[2], result40 = list1[3], result41 = list2[3],result50 = list1[4], result51 = list2[4])

  
@app.route('/graduatealgo')
def graduatealgo():
    data = pd.read_csv('WebScraped_data\csv\processed_data.csv')
    data.drop(data.columns[data.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    greV = float(request.args.get("greV"))
    greQ = float(request.args.get("greQ"))
    greA = float(request.args.get("greA")) 
    cgpa = float(request.args.get("cgpa"))
    testSet = [[greV, greQ, greA, cgpa]]
    test = pd.DataFrame(testSet)
    k = 7
    result,neigh = knn(data, test, k)
    list1 = []
    list2 = []
    for i in result:
        list1.append(i[0])
    for i in result:
        list2.append(i[1])
    for i in list1:
        print(i)
    return '''
        <html>
            <head>
                <title>University Recommendation Application</title>
                
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">
                <link href="http://getbootstrap.com/examples/jumbotron-narrow/jumbotron-narrow.css" rel="stylesheet">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous" />

                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
            </head>
            <body>
                <div class="container">     
                        <h2 style="text-align: center">Top-5 Graduate Recommended Universities</h2>
                        <br>
                        <p class="lead"></p>
                          <p>The Top-5 Graduate Recomended Universities based on your Gre Scores & CGPA are </p>
                          <br>

                            <table class="table table-striped"> 
                            <tr><td><h4>S.No</h4></td><td><h4>University</h4></td></tr>
                            <tr><td><p>1. </p></td><td>{result10}</td></tr>
                            <tr><td><p>2. </p></td><td>{result20}</td></tr>
                            <tr><td><p>3. </p></td><td>{result30}</td></tr>
                            <tr><td><p>4. </p></td><td>{result40}</td></tr>
                            <tr><td><p>5. </p></td><td>{result50}</td></tr>
                            </table>
                    
     

                    <p align="center">
                    <a class="btn btn-primary" href="/" role="button">Home</a>
                    <p>
                    
                </div>
            </body>
        </html>
            '''.format(result10 = list1[0], result20 = list1[1],result30 = list1[2], result40 = list1[3],result50 = list1[4])
            
            
            

if __name__ == "__main__":
    app.run(debug=True)
