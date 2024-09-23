from src import db

class User(db.Model):
    ''' Class that models users in blog app'''

    __tablename__ = 'user'
    # Primary Key
    username = db.Column('username', db.String(100), primary_key = True)
    password = db.Column('password', db.String(162), nullable = False)
    first_name = db.Column('first_name', db.String(100), nullable = False)
    second_name = db.Column('second_name', db.String(100), nullable = False)
    birthday = db.Column('birthday', db.Date, nullable = False)

    # Posts
    posts = db.relationship('Post', back_populates = 'user')


    def __init__(self,
                 username,
                 password,
                 first_name,
                 second_name,
                 birthday):
        '''Constructor'''
        self.username = username
        self.password = password
        self.first_name = first_name
        self.second_name = second_name
        self.birthday = birthday


    def __repr__(self) -> str:
        return f'{self.username}: {self.first_name} {self.second_name}'
