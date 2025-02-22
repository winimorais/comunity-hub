from flask import render_template, flash, request, redirect, url_for, abort
from comunityhub import app, database, bcrypt
from comunityhub.forms import LoginForm, CreateAccountForm, ProfileEditForm, CreatePostForm
from comunityhub.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/contact-details')
def contact_details():
    return render_template('contact-details.html')


@app.route('/users')
@login_required
def users():
    users_list = User.query.all()
    return render_template('users.html', users_list=users_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = LoginForm()
    form_creat_account = CreateAccountForm()
    if form_login.validate_on_submit() and 'login_submit' in request.form:
        user = User.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=form_login.remember_me.data)
            flash(f'Login successful for e-mail: {form_login.email.data}', 'alert-success')
            next_param = request.args.get('next')
            if next_param:
                return redirect(next_param)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Invalid login credentials. Please verify your email and password and try again.', 'alert-danger')
    if form_creat_account.validate_on_submit() and 'submit' in request.form:
        cript_password = bcrypt.generate_password_hash(form_creat_account.password.data)
        user = User(username=form_creat_account.username.data, email=form_creat_account.email.data,
                    password=cript_password)
        database.session.add(user)
        database.session.commit()
        flash(f'Registration successful for e-mail: {form_creat_account.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_creat_account=form_creat_account)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'Logout successful. See you next time!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    profile_photo = url_for('static', filename='profile_photos/{}'.format(current_user.profile_photo))
    return render_template('profile.html', profile_photo=profile_photo)


@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def creat_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post created successfully', 'alert-success')
        return redirect(url_for('home'))
    return render_template('creat-post.html', form=form)


def photo_save(photo):
    code = secrets.token_hex(8)
    name, type = os.path.splitext(photo.filename)
    file_name = name + code + type
    complete_path = os.path.join(app.root_path, 'static/profile_photos', file_name)
    size = (400, 400)
    reduced_image_size = Image.open(photo)
    reduced_image_size.thumbnail(size)
    reduced_image_size.save(complete_path)
    return file_name


def update_courses(form):
    courses_list = []
    for field in form:
        if field.name.startswith('course_') and field.data:
            courses_list.append(field.label.text)
    return ';'.join(courses_list)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = ProfileEditForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.profile_photo.data:
            photo_name = photo_save(form.profile_photo.data)
            current_user.profile_photo = photo_name
        current_user.courses = update_courses(form)
        database.session.commit()
        flash('Profile updated successfully', 'alert-success')
        return redirect(url_for('profile'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    profile_photo = url_for('static', filename='profile_photos/{}'.format(current_user.profile_photo))
    return render_template('profile-edit.html', profile_photo=profile_photo, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def show_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        form = CreatePostForm()
        if request.method == 'GET':
            form.title.data = post.title
            form.body.data = post.body
        elif form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            database.session.commit()
            flash('Post updated successfully', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/delete', methods=['GET', 'POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        database.session.delete(post)
        database.session.commit()
        flash('Post deleted successfully', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
