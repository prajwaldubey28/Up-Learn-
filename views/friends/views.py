from utils import *

friends_ = Blueprint('friends', __name__)

@friends_.route("/friends", methods = ["GET", "POST"])
@login_required
def friends():
    users = UserModel.query.all()
    friends = FriendModel.query.all()
    user = UserModel.query.filter_by(name = session["username"]).first()
    data = {
        "username": session["username"],
        "friends": friends,
        "all_users": users,
        "user": user
    }
    return render_template("friends/friends.html", data = data)

@friends_.route("/friends/send-request/<name>", methods = ["GET", "POST"])
@login_required
def send_request(name):
    friends = FriendModel(user1 = session["username"], user2 = name, status = 0)
    db.session.add(friends)
    db.session.commit()
    return redirect("/friends")

@friends_.route("/friends/accept/<user1>/<user2>", methods = ["GET", "POST"])
@login_required
def accept(user1, user2):
    friends = FriendModel.query.filter_by(user1 = user1, user2 = user2).first()
    friends.status = 1
    db.session.add(friends)
    db.session.commit()
    return redirect("/friends")

@friends_.route("/friends/reject/<user1>/<user2>", methods = ["GET", "POST"])
@login_required
def reject(user1, user2):
    friends = FriendModel.query.filter_by(user1 = user1, user2 = user2).delete()
    db.session.commit()
    return redirect("/friends")

@friends_.route("/friends/remove/<user1>/<user2>", methods = ["GET", "POST"])
@login_required
def remove(user1, user2):
    friends = FriendModel.query.filter_by(user1 = user1, user2 = user2).delete()
    db.session.commit()
    return redirect("/user-profile/{}".format(session["username"]))