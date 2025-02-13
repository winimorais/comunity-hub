from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from comunityhub.models import User
from flask_login import current_user


class CreateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    confirmation = PasswordField('Confirm Password',
                                 validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'This email address is already in use. Please use a different email address or log in.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    remember_me = BooleanField('Remember me')
    login_submit = SubmitField('Login')


class ProfileEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_photo = FileField('Update profile photo', validators=[FileAllowed(['jpg', 'png'])])
    course_python = BooleanField('Python Developer')
    course_java = BooleanField('Java Developer')
    course_php = BooleanField('PHP Developer')
    course_go = BooleanField('Go Developer')
    course_javascript = BooleanField('React Developer')
    course_sql = BooleanField('SQL Developer')
    course_aws = BooleanField('AWS Cloud Developer')
    profile_edit_submit = SubmitField('Confirm Edit')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'This email address is already in use. Please use a different email address.')
