from flask import Blueprint, request, g, redirect, url_for, \
					abort, render_template, flash, current_app
from flaskext.login import login_required, current_user
from jinja2 import TemplateNotFound
from main.users import constants as USER
from main.users.helpers import access_level_required
from main.blog.models import Post
from main.comments.models import Comment

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/')
@login_required
@access_level_required(USER.ADMIN)
def index():
	"""
		Display the main admin console.
	"""
	posts = g.db_session.query(Post).filter_by(published=False).all()
	comments = g.db_session.query(Comment).filter_by(approved=False).all()


	flash('Welcome!')

	try:
		return render_template('admin_index.html', posts=posts, comments=comments)
	except TemplateNotFound:
		abort(404)