from src import db
from datetime import datetime

class Post(db.Model):
    ''' Class that models users in blog app'''

    __tablename__ = 'post'
    # Primary Key
    id = db.Column('id', db.Integer, primary_key = True)
    author = db.Column(db.String(100), db.ForeignKey('user.username'))
    access = db.Column('access', db.Boolean, default = True)
    title = db.Column('title', db.String(100), nullable = False)
    img = db.Column('img', db.Text, nullable = True)
    text = db.Column('text', db.Text, nullable = True)
    likes = db.Column('likes', db.Integer, nullable = False, default = 0)
    date = db.Column('date', db.DateTime, nullable = False)

    # Posts
    user = db.relationship('User', back_populates = 'posts')


    def __init__(self,
                 title,
                 text,
                 access):
        self.title = title
        self.text = text
        self.access = access
        self.date = datetime.now()


    def __repr__(self) -> str:
        return f'{self.title}: {self.date}'
