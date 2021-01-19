from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length



class RegisterUserForm(FlaskForm):
    """ Form for creating user """
    username = StringField("Username",
        validators=[InputRequired()])
    password = PasswordField("Password",
        validators=[InputRequired()])
    email = StringField("Email",
        validators=[InputRequired(), Email()])
    first_name = StringField("First Name",
        validators=[InputRequired()])
    last_name = StringField("Last Name",
        validators=[InputRequired()])

class LoginUserForm(FlaskForm):
    """ Form for logging in user """
    username = StringField("Username",
        validators=[InputRequired()])
    password = PasswordField("Password",
        validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """ Form for adding/editing Feedback """
    title = StringField("Title",
        validators=[InputRequired(),
        Length(min=1, max=100)])
    content = StringField("Content",
        validators=[InputRequired()])
