from flask import render_template,redirect,url_for,flash,request
from . import auth
from ..models import User
from flask_login import login_user,logout_user,login_required
from .forms import RegistrationForm,LoginForm
from ..email import mail_message
from .. import db

@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()

       # mail_message("Welcome to pitch","email/welcome_user",user.email,user=user)

        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register.html',registration_form = form)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    """
        Handle requests to the /login route
        Log an employee in through the login form
        """

    login_form = LoginForm()
    if login_form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database

        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            # log employee in

            login_user(user, login_form.remember.data)

            # redirect to the index page after login

            return redirect(request.args.get('next') or url_for('main.new_pitch'))

        # when login details are incorrect

        flash('Invalid username or Password')

    title = "login"

    # load login template

    return render_template('auth/login.html',login_form = login_form,title=title)


@auth.route('/logout')
@login_required
def logout():
    """
        Handle requests to the /logout route
        Log an employee out through the logout link
        """

    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for("main.index"))    