# Import flask dependencies
from flask import request, render_template, \
    flash, g, session, redirect, url_for
from flask_login import login_user
# Import password / encryption helper tools
from werkzeug.security import generate_password_hash, check_password_hash

# blueprint
from . import auth

# Import the database object from the main app module
from .. import db

# Import module forms
from .forms import LoginForm, RegistrationForm

# Import module models (i.e. User)
from app.models import User


# Set the route and accepted methods
@auth.route('/login/', methods=['GET', 'POST'])
def login():
    # If sign in form is submitted
    form = LoginForm()

    # Verify the sign in form
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        print(user.username)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('auth.user'))
    flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/register/', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        flash('You can Login now')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/user/', methods=['GET'])
def user():
    return render_template("auth/user.html")
