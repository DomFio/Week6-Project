from flask import Blueprint, render_template
from flask_login.utils import login_required

"""
Note that in the code below, some arguments are specified when creating the Blueprint Object
The first argument, "site", is the Blueprints name
which is used by flasks routing mechanism

The second argument, __name__ is the blueprints import name
which flask uses to locate the blueprints resources
"""



site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')