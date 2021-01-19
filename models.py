"""Models for Feedback app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """ Connect to a database """

    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User Model """

    __tablename__ = "users"

    id = db.Column(db.Integer,
        primary_key = True,
        autoincrement = True)
    username = db.Column(db.String(20),
        nullable = False,
        unique = True)
    password = db.Column(db.Text,
        nullable = False)
    email = db.Column(db.String(50),
        nullable = False,
        unique = True)
    first_name = db.Column(db.String(30),
        nullable = False)
    last_name = db.Column(db.String(30),
        nullable = False)

    feedback = db.relationship('Feedback', cascade="all,delete")

    @classmethod
    def register_query(cls, username, password, 
            email, first_name, last_name):
        """ Create new User with hashed
        password & return new User """

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username,
            password=hashed_utf8, email=email,
            first_name=first_name,
            last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.
        Return user if valid; else return False."""

        existing_user = User.query.filter_by(username=username).first()

        if existing_user and bcrypt.check_password_hash(
                existing_user.password, password):
            return existing_user
        else:
            return False

    @classmethod
    def lookup_username_query(cls, username):
        """Ensure user ID exists """
        user = User.query.filter_by(username=username).one()
        return user

    @classmethod
    def delete_user_query(cls, user):
        db.session.delete(user)
        db.session.commit()
        return

class Feedback(db.Model):
    """ Feedback Model """

    __tablename__ = "feedback"

    id = db.Column(db.Integer,
        primary_key = True,
        autoincrement = True)
    title = db.Column(db.String(100),
        nullable = False)
    content = db.Column(db.Text,
        nullable = False)
    username = db.Column(db.String(20),
        db.ForeignKey('users.username'),
        nullable = False)

    user = db.relationship('User')

    @classmethod
    def feedback_add_query(cls, username, title, content):
        feedback = Feedback(username= username, title=title, content=content)
        db.session.add(feedback)
        db.session.commit()
        return

    @classmethod
    def lookup_feedback_query(cls, feedback_id):
        feedback = Feedback.query.get_or_404(feedback_id)
        return feedback

    @classmethod
    def update_query(cls, feedback):
        db.session.commit()
        return

    @classmethod
    def delete_feedback_query(cls, feedback):
        db.session.delete(feedback)
        db.session.commit()
        return
