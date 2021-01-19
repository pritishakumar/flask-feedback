"""Flask app for Feedback Authentication"""

from flask import Flask, request, redirect, render_template, session
from models import db, connect_db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterUserForm, LoginUserForm, FeedbackForm
from flask_bcrypt import Bcrypt




app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

bcrypt = Bcrypt(app)

connect_db(app)

@app.route("/")
def homepage():
    """ Redirects to /register """
    return redirect("/register")

@app.route("/register", methods = ["GET", "POST"])
def register_user():
    """ GET: renders the register form
    POST: extracts the data, creates a new user
    and redirects to secret page """
    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register_query(username, password, 
            email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(f"/users/{username}")

    else:
        return render_template("register-form.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login_user():
    """ GET: renders the login form
    POST: extracts the data, validates the user
    and redirects to secret page """

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{username}")
        else:
            return redirect("/login")

    else:
        return render_template("login-form.html", form=form)

@app.route("/logout")
def logout():
    """ Clears the session of the username and redirects to /"""
    session.pop("username")
    return redirect("/")

@app.route("/users/<username>")
def user_detail(username):
    """ Renders the user detail page if the correct user is 
    logged in, as per the Flask session entry, otherwise redirects
    to / """
    if "username" in session:
        user = User.lookup_username_query(session["username"])
        if username == user.username:
            return render_template("user-detail.html", user=user)
        else:
            return redirect(f"/users/{user.username}")
    return redirect("/register")

@app.route("/users/<username>/delete", methods=["POST"])
def user_delete(username):
    """ Deletes a user from the database if it is confirmed that 
    same user is placing the request """
    if "username" in session:
        user = User.lookup_username_query(session["username"])
        if username == user.username:
            User.delete_user_query(user)
            session.pop("username")
    return redirect("/")

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def feedback_add(username):
    """ Renders the form to add or adds feedback as the user who is 
    confirmed to be logged in """
    if "username" in session:
        user = User.lookup_username_query(session["username"])
        form = FeedbackForm()

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            Feedback.feedback_add_query(username, title, content)
            return redirect(f"/users/{username}")
        return render_template("feedback-add.html", user=user, form=form)
    return redirect("/")

@app.route("/feedback/<feedback_id>/update", methods=["GET", "POST"])
def feedback_update(feedback_id):
    """ Renders the form to update, or updates the specific feedback, if it is 
    confirmed to be done by the original user who created the feedback """
    if "username" in session:
        user = User.lookup_username_query(session["username"])
        feedback = Feedback.lookup_feedback_query(feedback_id)
        if feedback.username == user.username:
            form = FeedbackForm(obj=feedback)

            if form.validate_on_submit():
                    feedback.title = form.title.data
                    feedback.content = form.content.data
                    Feedback.update_query(feedback)
                    return redirect(f"/users/{user.username}")
            return render_template("feedback-edit.html", user=user, form=form)
    return redirect("/")

@app.route("/feedback/<feedback_id>/delete", methods=["POST"])
def feedback_delete(feedback_id):
    """ Deletes a specific feedback if it is confirmed to be 
    done by the original user who created the feedback  """
    if "username" in session:
        user = User.lookup_username_query(session["username"])
        feedback = Feedback.lookup_feedback_query(feedback_id)
        if feedback.username == user.username:
            Feedback.delete_feedback_query(feedback)
            return redirect(f"/users/{user.username}")

    return redirect("/")