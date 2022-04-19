from utils import *

authentication_ = Blueprint('authentication', __name__)

ts = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))

@authentication_.route("/authentication")
def auth():
    return redirect("/authentication/login")

@authentication_.route("/authentication/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = UserModel.query.filter_by(email = email).first()
        if user is None:
            flash("User with this email not found. Please try again.")
            return redirect("/authentication/login")
        if user.check_password(password):
            login_user(user)
            session["username"] = current_user.name
            session["id"] = current_user.id
            return redirect('/')
        else:
            flash("Password incorrect. Please try again.")
            return redirect("/authentication/login")
    return render_template("authentication/login.html")

@authentication_.route("/authentication/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if len(name) < 7:
            flash("Username should be greater than 6 characters.")
            return redirect("/authentication/register")
        if UserModel.query.filter_by(name=name).first():
            flash("Username already Present. Please try with other username.")
            return redirect("/authentication/register")
        if UserModel.query.filter_by(email=email).first():
            flash("Email already Present. Please try with other email.")
            return redirect("/authentication/register")
        if len(password) < 7:
            flash("Password should be greater than 6 characters.")
            return redirect("/authentication/register")
        if password != confirm_password:
            flash("Passwords did'nt matched.")
            return redirect("/authentication/register")
        user = UserModel(email=email, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Account created. Now Login.")
        return redirect('/authentication/login')
    return render_template("authentication/register.html")

@authentication_.route("/authentication/forgot-password", methods = ['GET', 'POST'])
def forgot():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        email = request.form["email"]
        user = UserModel.query.filter_by(email = email).first()
        if user is None:
            flash("User with this email not found. Please try again.")
            return redirect("/authentication/forgot-password")
        token = ts.dumps(email, salt = "recover-key")
        db.session.add(user)
        db.session.commit()
        send_mail(email, token)
        flash("An Email with password reset link is sent to your email - {}. It will expire in 5 minutes.".format(email))
        return redirect("/authentication/forgot-password")
    return render_template("authentication/forgot-password.html")

@authentication_.route("/authentication/reset/<token>", methods = ['GET', 'POST'])
def reset_with_token(token):
    if current_user.is_authenticated:
        return redirect('/')
    try:
        email = ts.loads(token, salt="recover-key", max_age = 300)
    except:
        flash("URL Expired.")
        return render_template("authentication/reset.html", url = "!")
    if request.method == "POST":
        user = UserModel.query.filter_by(email = email).first()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if len(password) < 7:
            flash("Password should be greater than 6 characters.")
            return redirect("/authentication/reset/{}".format(token))
        if password != confirm_password:
            flash("Passwords did'nt matched.")
            return redirect("/authentication/reset/{}".format(token))
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Password reset successful. Now login.")
        return redirect("/authentication/login")
    user = UserModel.query.filter_by(email = email).first()
    if user.password_hash is not None:
        action_url = "/authentication/reset/{}".format(token)
        return render_template("authentication/reset.html", url = action_url)
    else:
        flash("URL Expired.")
        return render_template("authentication/reset.html", url = "#")

@authentication_.route('/authentication/logout')
@login_required
def logout():
    logout_user()
    session.pop("username", None)
    session.pop("id", None)
    flash("Logout Successful.")
    return redirect('/authentication/login')