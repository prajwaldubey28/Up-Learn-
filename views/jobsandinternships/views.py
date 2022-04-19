
import re
from utils import *
from models import RepliesModel

jobsandinternships_ = Blueprint('jobsandinternships', __name__)

@jobsandinternships_.route("/jobs-internships", methods = ["GET", "POST"])
@login_required
def jobsandinternships():
    user = UserModel.query.filter_by(name = session["username"]).first()
    internships = InternshipModel.query.all()
    data = {
        "username": session["username"],
        "user": user,
        "internships": internships,
    }
    return render_template("jobs-and-internships/jobs_and_internships.html", data=data)

@jobsandinternships_.route("/jobs", methods = ["POST"])
@login_required
def jobs():
    internship_name = request.form["internship_name"]
    rte_body = request.form["rte_body"]
    arr = []
    for f in request.files.getlist('files[]'):
        name = f.filename
        extension = name.split(".")[-1]
        filename = secrets.token_hex(8) + "." + extension
        arr.append(filename)
        f.save(os.path.join('static/Uploads/internship-files', filename))
    attachments = " ".join([i for i in arr])
    date = getCurrentDate()
    internship = InternshipModel(
        internship_name = internship_name,
        attachments = attachments,
        rte_body = rte_body,
        user_name = session["username"],
        date = date
    )
    db.session.add(internship)
    db.session.commit()
    return redirect("/jobs-internships")

@jobsandinternships_.route("/job/<id>", methods = ["GET", "POST"])
@login_required
def job_id(id):
    internship = InternshipModel.query.filter_by(id = id).first()
    user = UserModel.query.filter_by(name = session["username"]).first()

    replies = RepliesModel.query.filter_by(internship_id = id).all()

    count = len(replies)


    data = {
        "user": user,
        "internship": internship,
        "id": id,
        "count": count,
        "replies": replies
    }
    return render_template("jobs-and-internships/jobs.html", data=data)



@jobsandinternships_.route("/internships", methods = ["POST"])
@login_required
def internships():
    internship_name = request.form["internship_name"]
    rte_body = request.form["rte_body"]
    arr = []
    for f in request.files.getlist('files[]'):
        name = f.filename
        extension = name.split(".")[-1]
        filename = secrets.token_hex(8) + "." + extension
        arr.append(filename)
        f.save(os.path.join('static/Uploads/internship-files', filename))
    attachments = " ".join([i for i in arr])
    
    date = getCurrentDate()
    internship = InternshipModel(
        internship_name = internship_name,
        attachments = attachments,
        rte_body = rte_body,
        user_name = session["username"],
        date = date
    )
    db.session.add(internship)
    db.session.commit()
    return redirect("/jobs-internships")

@jobsandinternships_.route("/internship/<id>", methods = ["GET", "POST"])
@login_required
def internship_id(id):
    internship = InternshipModel.query.filter_by(id = id).first()
    user = UserModel.query.filter_by(name = session["username"]).first()

    replies = RepliesModel.query.filter_by(internship_id = id).all()
    attahments = internship.attachments

    print(attahments)

    data = {
        "user": user,
        "internship": internship,
        "id": id,
        "replies": replies
    }
    return render_template("jobs-and-internships/internship.html", data=data)


@jobsandinternships_.route("/internship/reply/<id>", methods = ["GET", "POST"])
@login_required
def internship_reply(id):

    rte_body = request.form["editordata"]
    date = getCurrentDate()

    reply_internship = RepliesModel(
        internship_id = id,
        date = date,
        message = rte_body,
        user_name = session["username"],
    )
    db.session.add(reply_internship)
    db.session.commit()
    
    return redirect("/internship/{}".format(id))