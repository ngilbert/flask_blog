from flask import Blueprint, request, g, redirect, url_for, \
				abort, render_template, flash, current_app
from flaskext.login import login_required, login_user, logout_user, current_user
from models import User, AuthUser
from forms import LoginForm, RegistrationForm
import constants
import hashlib



""" ---------------------------------------------------------------------------
	P R O P E R T I E S 
--------------------------------------------------------------------------- """
users = Blueprint('users', __name__, template_folder='templates')


""" ---------------------------------------------------------------------------
	F U N C T I O N S
--------------------------------------------------------------------------- """
def hash_password(password):
    """
        Hash a plain text password.
    """
    hashed_pw = hashlib.sha512(SECRET_KEY)
    hashed_pw.update(password)
    return hashed_pw.hexdigest()

def generate_key(salt):
    """
        Creates a SHA1 hex key.
    """
    key = hashlib.sha1()
    key.update(salt)
    return key.hexdigest()

def is_access_allowed(access_level):
	"""
		Determines if current user has access.

		TODO:  Where to put this method.
	"""
	return current_user.role <= access_level


@users.route('/login', methods=['GET', 'POST'])
def login():
	"""
		Log user in or display login form.
	"""
	form = LoginForm(request.form)

	if request.method == 'POST' and form.validate():
		#TODO:  Hash password
		hashed_pw = form.password.data
		#hashed_pw = hash_password(form.password.data)
		user = g.db_session.query(User).filter_by(email=form.email.data, password=hashed_pw).first()
		if user is not None:
			auth_user = AuthUser(user.id, user.username, user.role, user.confirmed)

			if login_user(auth_user):
				flash(u"Logged in!")
				return redirect(request.args.get('next') or url_for('index'))
			else:
				flash(u"Sorry, but you could not be logged in.")
		else:
			flash(u"Invalid login credentials.")

	return render_template('login.html', form=form)


@users.route('/confirm/<string:key>', methods=['GET'])
def confirm(key):
	"""
		Process user confirmation.
	"""
	# Check if key exists in database
	user = g.db_session.query(User).filter_by(confirmation_key=key).first()

	if user is not None:
		user.confirmation_key = ''
		user.confirmed = True
		auth_user = AuthUser(user.id, user.username, user.role, user.confirmed)

		if login_user(auth_user):
			flash(u"Thanks for confirming your email address.")	
			return render_template('register_thanks.html')
		else:
			flash(u"Sorry, but you could not be logged in.")
	else:
		flash(u"Invalid confirmation key.")

	return render_template('register.html', form=RegistrationForm())


@users.route('/register', methods=['GET', 'POST'])
def register():
	"""
		Register a new user.

		POST - Checks if username and email already exist.
		GET - Displays registration from.
	"""
	if current_user is not None and current_user.confirmed is True:
		flash(u"User is already confirmed.")
		return redirect(url_for('index'))

	form = RegistrationForm(request.form)
	username_exists = False
	email_exists = False

	if request.method == 'POST' and form.validate():
		# check is username is available and email address hasn't already been registered
		username_exists = g.db_session.query(User).filter_by(username=form.username.data).first() is not None
		email_exists = g.db_session.query(User).filter_by(email=form.email.data).first() is not None

		if username_exists is False and email_exists is False:
			confirmation_key = generate_key(form.username.data)
			new_user = User(form.username.data, form.email.data, form.password.data, constants.USER, confirmation_key)
			g.db_session.add(new_user)
			#TODO: email user with confirmation link
			flash(u"A confirmation has been sent to your email address.  Please follow the link it contains.")
			return render_template('register_confirm.html')
		elif email_exists is True:
			message = u"Email address already registered."
		elif username_exists is True:
			message = u"Username already exists."

	flash(message)
	return render_template('register.html', form=form)


@users.route('/logout')
@login_required
def logout():
	"""
		Log the user out.
	"""
	current_app.logger.debug('Logging out user')
	current_app.logger.debug('current user id:' + current_user.get_id())
	logout_user()
	flash(u"Logged out.")
	return redirect(url_for('index'))
