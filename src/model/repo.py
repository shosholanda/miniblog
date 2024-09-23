import datetime as dt

from sqlalchemy import func, or_
from sqlalchemy.sql import text
from src.model.user import User
from src.model.post import Post


from src import db

def get_user(username):
    '''Returns the username as python object'''
    session = db.session()
    query = text(f"SELECT * FROM user WHERE username = '{username}'")
    cursor = session.execute(query).cursor
    return cursor.fetchone()

def get_all_public_posts():
    '''Returns all public posts'''
    return Post.query.filter(Post.access == 1)

def get_post_by_id(id_post):
    return Post.query.get(id_post)

def get_posts_by_access(user, access):
    return Post.query.filter(Post.access == access, Post.author == user)

def get_birthdays(days):
    '''Gets all birthdays within the range days '''
    dateFrom = dt.date.today()
    dateTo = dt.date.today() + dt.timedelta(days=days)
    thisYear = dateFrom.year
    nextYear = dateFrom.year +1
    return User.query.filter(
        or_(
            func.STR_TO_DATE(func.concat(func.DATE_FORMAT(User.birthday, "%d%m"), thisYear), "%d%m%Y").between(dateFrom, dateTo),
            func.STR_TO_DATE(func.concat(func.DATE_FORMAT(User.birthday, "%d%m"), nextYear), "%d%m%Y").between(dateFrom, dateTo)
        )
    )

def validate_user_and_password(username, password):
    session = db.session()
    query = text(f"SELECT * FROM user WHERE username='{username}' AND password='{password}'")
    try:
        cursor = session.execute(query).cursor
    except:
        return False
    return cursor.fetchone()


def add(entity):
    '''Adds the model to its respective table'''
    db.session.add(entity)
    db.session.commit()

def remove(entity):
    '''Removes the model to its respective table'''
    db.session.delete(entity)
    db.session.commit()

