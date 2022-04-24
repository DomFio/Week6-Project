from flask import Blueprint, render_template, request, redirect, url_for, flash
from skating_inventory.models import User, db, check_password_hash
from skating_inventory.forms import UserLoginForm

# Imports for Flask_Login
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User(email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account: {email}', 'user-created')


            return redirect(url_for('site.home'))
            
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('signup.html', form=form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            print('hello')
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                print('hello2')
                flash('You were succesfully logged in: Via email/password', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Your email/password is incorret', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')
    return render_template('signin.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))