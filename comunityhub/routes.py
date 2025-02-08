from flask import render_template, flash, request, redirect, url_for
from comunityhub import app, database, bcrypt
from comunityhub.forms import FormLogin, CreateAccountForm
from comunityhub.models import User
from flask_login import login_user, logout_user, current_user

users_list = ['Ana', 'Bruna', 'Pedro', 'Joao', 'Clara']


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contact-details')
def contact_details():
    return render_template('contact-details.html')


@app.route('/users')
def users():
    return render_template('users.html', users_list=users_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_creat_account = CreateAccountForm()

    if form_login.validate_on_submit() and 'login_submit' in request.form:
        user = User.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=form_login.remember_me.data)
            flash(f'Login successful for e-mail: {form_login.email.data}', 'alert-success')
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
def logout():
    logout_user()
    flash(f'Logout successful. See you next time!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/post/create')
def creat_post():
    return render_template('creat-post.html')
