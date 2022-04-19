from utils import *

projects_ = Blueprint('projects', __name__)

@projects_.route("/projects", methods = ["GET", "POST"])
@login_required
def projects():
    id = session["id"]
    username = session["username"]
    if request.method == "POST":
        project_name = request.form["project_name"]
        project_description = request.form["project_description"]
        project_tags = request.form["project_tags"]
        project_link = request.form["project_link"]
        project = ProjectsModel(
            name = project_name, 
            description = project_description,
            tags = project_tags,
            link = project_link,
            user_id = id,
            user_name = username
        )
        db.session.add(project)
        db.session.commit()
        return redirect("/projects")
    projects = ProjectsModel.query.all()[::-1]
    user = UserModel.query.filter_by(name = session["username"]).first()
    all_users = UserModel.query.all()
    data = {
        "username": username,
        "projects": projects,
        "my_id": int(id),
        "user": user,
        "all_users": all_users
    }
    return render_template("projects/projects.html", data=data)

@projects_.route("/projects/edit/<id>", methods = ["POST"])
@login_required
def projects_edit(id):
    project = ProjectsModel.query.filter_by(id = id).first()
    project.name = request.form["project_name"]
    project.description =  request.form["project_description"]
    project.tags = request.form["project_tags"]
    project.link = request.form["project_link"]
    db.session.commit()
    return redirect("/projects")

@projects_.route("/project/<id>", methods = ["GET", "POST"])
@login_required
def project_id(id):
    project = ProjectsModel.query.filter_by(id = id).first()
    comments = CommentModel.query.filter_by(project_id = id)
    user = UserModel.query.filter_by(name = session["username"]).first()
    data = {
        "username": session["username"],
        "my_id": session["id"],
        "projects": project,
        "comments": comments,
        "user": user
    }
    return render_template("projects/project-details.html",  data=data)

@projects_.route("/project/comment/<id>", methods = ["POST"])
@login_required
def project_comment(id):
    comment = request.form["comment"]

    string = getCurrentDate()
    comment = CommentModel(comment=comment, project_id=id, user_id=session["id"], user_name=session["username"], time = string)
    db.session.add(comment)
    db.session.commit()
    return redirect("/project/{}".format(id))

@projects_.route("/project/delete/<id>", methods = ["POST", "GET"])
@login_required
def delete(id):
    dele = ProjectsModel.query.filter_by(id = id).first()
    comment = CommentModel.query.filter_by(project_id = id).all()
    for i in comment:
        db.session.delete(i)
    db.session.delete(dele)
    db.session.commit()
    return redirect("/projects")