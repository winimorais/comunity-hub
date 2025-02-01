from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class CreateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    confirmation = PasswordField('Confirm Password',
                                 validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')


class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    remember_me = BooleanField('Remember me')
    login_submit = SubmitField('Login')