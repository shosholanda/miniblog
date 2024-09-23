import functools
import os

from flask import (render_template, Blueprint, g, redirect, request, session, url_for)

# Upload files secure
from werkzeug.utils import secure_filename
from src.controller.auth import requires_login

# Maped rows to objects
from src.model.user import User
from src.model.post import Post
# import querys
from src.model.repo import *
from src import app

# Endpoint para la función de autenticación y registro de usuarios
profile = Blueprint('profile', __name__, url_prefix='/profile')

@profile.route('/<user>', methods=['GET', 'POST'])
@requires_login
def main(user):
    '''Gets the user information and can update info when update'''
    user = get_user(user)
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        birthday = request.form.get('birthday')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        user.first_name = first_name
        user.second_name = second_name
        user.birthday = birthday

        if old_password and new_password:
            if old_password == user.password:
                user.password = new_password
            else:
                flash('Las contraseñas no coinciden')

        add(user)
    return render_template('blog/profile.html',
                           user = user)

@profile.route('/create', methods=['GET', 'POST'])
@requires_login
def create():
    '''This person creates a post'''
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text').strip()
        img = request.files['img']
        access = 'access' in request.form

        post = Post(title, text, access)
        post.author = session['user']#:)

        if img:
            filename = secure_filename(img.filename)
            abs_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img.save(abs_path)
            post.img = abs_path[5+8:] #LMAO

        add(post)
        return redirect(url_for('home.main'))

    return render_template('blog/create.html')

@profile.route('/update/<int:id_post>', methods=['GET', 'POST'])
@requires_login
def update(id_post):
    '''Updates a post by this user'''
    post = get_post_by_id(id_post)
    return render_template('blog/update.html', post = post)

@profile.route('/delete/<int:id_post>', methods=['GET', 'POST'])
@requires_login
def delete(id_post):
    '''Deletes a post by this user'''
    post = get_post_by_id(id_post)
    remove(post)
    return redirect(url_for('profile.main', user = post.author))
