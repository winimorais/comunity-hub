from flask import render_template, flash, request, redirect, url_for
from comunityhub import app
from comunityhub.forms import FormLogin, CreateAccountForm

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
        flash(f'Login successful for e-mail: {form_login.email.data}', 'alert-success')
        return redirect(url_for('home'))

    if form_creat_account.validate_on_submit() and 'submit' in request.form:
        flash(f'Registration successful for e-mail: {form_creat_account.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_creat_account=form_creat_account)
