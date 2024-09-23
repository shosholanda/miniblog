import functools, os, datetime, requests, json

from flask import (jsonify, render_template, Blueprint, g, redirect, request, session, url_for)

from werkzeug.utils import secure_filename
from src.controller.auth import requires_login

# Maped rows to objects
from src.model.user import User
from src.model.post import Post
from src.model.repo import *
from src import app

# Endpoint para la función de autenticación y registro de usuarios
home = Blueprint('home', __name__, url_prefix='/home')

@home.route('/', methods=['GET', 'POST'])
@requires_login
def main():
    '''Method to get the feed'''
    posts = list(get_all_public_posts())[::-1]
    birthdays = get_birthdays(30)
    api_url = 'https://catfact.ninja/fact'
    response = requests.get(api_url).content.decode('utf8') #Trucos sobre trucos
    response = json.loads(response)
    # s = json.dumps(response, indent=4, sort_keys=True)
    return render_template('blog/home.html', posts = posts, birthdays = birthdays, today = datetime.datetime.now(), response = response)

@home.route('/<user>/<access>', methods=['GET'])
def my_posts(user, access):
    '''See the public and private post of this user'''
    if access == 'private':
        access = False
    else:
        access = True
    posts = list(get_posts_by_access(user, access))[::-1]
    birthdays = get_birthdays(30)
    api_url = 'https://catfact.ninja/fact'
    response = requests.get(api_url).content.decode('utf8') #Trucos sobre trucos
    response = json.loads(response)
    today = datetime.datetime.now()
    return render_template('blog/home.html', posts = posts, birthdays = birthdays, today = today, response = response)

@home.route('/<int:id_post>')
@requires_login
def post(id_post):
    '''Gets a single post and performs operations on it'''
    post = get_post_by_id(id_post)
    api_url = 'https://catfact.ninja/fact'
    response = requests.get(api_url).content.decode('utf8') #Trucos sobre trucos
    birthdays = get_birthdays(30)
    response = json.loads(response)
    today = datetime.datetime.now()
    return render_template('blog/post.html', post = post, id_post = id_post, birthdays = birthdays, response = response, today= datetime.datetime.now())

@home.route('/like', methods=['POST'])
@requires_login
def like():
    '''Method to send a like when like button'''
    if request.method == 'POST':
        body = request.json#['body'] <- for postman
        id_post = body['id']
        post = get_post_by_id(id_post)
        post.likes = post.likes +1;
        add(post)
    return redirect(url_for('home.post', id_post = id_post))


@home.route('/get-likes/<int:id_post>', methods=['GET'])
@requires_login
def get_likes(id_post):
    '''Method to get the last number of likes in the post'''
    post = get_post_by_id(id_post);
    response = {'id': post.id,
                'likes': post.likes}
    return jsonify(response)

