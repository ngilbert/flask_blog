from flask import Blueprint, request, g, redirect, url_for, \
        abort, render_template, flash, current_app
from flaskext.login import login_required, current_user
import main.models as models
from jinja2 import TemplateNotFound


""" ---------------------------------------------------------------------------
    P R O P E R T I E S 
--------------------------------------------------------------------------- """
admin = Blueprint('admin', __name__, template_folder='templates')


""" ---------------------------------------------------------------------------
    F U N C T I O N S
--------------------------------------------------------------------------- """
@admin.route('/')
@login_required
def index():
    """
        Show the admin section is user is logged in.
    """
    posts = g.db_session.query(models.Post).all()
    #current_app.logger.debug('Rendering admin template')
    return render_template('admin.html', posts=posts)
