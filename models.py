from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

login = LoginManager()
db = SQLAlchemy()

class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    name = db.Column(db.String(100))
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(100))
    password_hash = db.Column(db.String())
    title = db.Column(db.Text)
    about_me = db.Column(db.Text)
    facebook = db.Column(db.String(100))
    linkedin = db.Column(db.String(100))
    github = db.Column(db.String(100))
    instagram = db.Column(db.String(100))
    profile_pic = db.Column(db.String(15))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ProjectsModel(UserMixin, db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    tags = db.Column(db.Text)
    link = db.Column(db.String(100))
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(100))

class CommentModel(UserMixin, db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    project_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(100))
    time = db.Column(db.String(100))

class FriendModel(UserMixin, db.Model):
    __tablename__ = 'friends'

    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Text)
    user2 = db.Column(db.Text)
    status = db.Column(db.Integer)

class InternshipModel(UserMixin, db.Model):
    __tablename__ = 'internships'

    id = db.Column(db.Integer, primary_key=True)
    internship_name = db.Column(db.Text)
    rte_body = db.Column(db.Text)
    attachments = db.Column(db.Text)
    image = db.Column(db.String(15))
    date = db.Column(db.String(100))
    user_name = db.Column(db.Text)

class RepliesModel(UserMixin, db.Model):
    __tablename__ = 'replies'

    id = db.Column(db.Integer, primary_key=True)
    internship_id = db.Column(db.Text)
    message = db.Column(db.Text)
    date = db.Column(db.String(100))
    attachments = db.Column(db.Text)
    user_name = db.Column(db.Text)

@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))