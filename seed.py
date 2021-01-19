from app import app
from models import db, User, Feedback

db.drop_all()
db.create_all()


def seed_database():
    """ Adds some default data into the database """
    u1 = User(username="pk" , password= '$2b$12$B0Hi6gI5LKlKPZmN.suGfOa1/gLfrB01zLn59SOGexoRYxH81NOe6', email= 'pk@gmail.com', first_name= 'P', last_name= 'K')
    db.session.add_all([u1])
    db.session.commit()
    f1 = Feedback(title="Great", content="Loved what you did with the routing!", username="pk")
    f2 = Feedback(title="Meh", content="I think we could've tightened this up a bit!", username="pk")
    db.session.add_all([f1, f2])
    db.session.commit()

seed_database()