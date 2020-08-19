# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm  # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError

# Import Form validators
from wtforms.validators import Required, Email, EqualTo
from wtforms.validators import Length
from wtforms.validators import DataRequired
from ..models import User

# Define the login form (WTForms)


class LoginForm(FlaskForm):
    email = StringField('Email Address', [Email(),
                                          DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, max=10)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=6, max=12)
    ])
    email = StringField('Email Address', [Email(),
                                          DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, max=10), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField(label='password_confirm', validators=[
        DataRequired(), Length(min=6, max=10)])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')