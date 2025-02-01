from flask import Flask, render_template, url_for
from forms import FormLogin, CreateAccountForm

app = Flask(__name__)

users_list = ['Ana', 'Bruna', 'Pedro', 'Joao', 'Clara']

app.config['SECRET_KEY'] = '353b63f85b8497def16c8e8c55db225a'

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contact-details')
def contact_details():
    return render_template('contact-details.html')

@app.route('/users')
def users():
    return render_template('users.html', users_list=users_list)

@app.route('/login')
def login():
    form_login = FormLogin()
    form_creat_account = CreateAccountForm()
    return render_template('login.html', form_login=form_login, form_creat_account=form_creat_account)


if __name__ == '__main__':
    app.run(debug=True)
