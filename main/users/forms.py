from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField, validators


class LoginForm(Form):
	"""
		The existing users login form.
	"""
	email = TextField('Email', [validators.Required()])
	password = PasswordField('Password', [validators.Required()])

	def __repr__(self):
		""" String representation of object. """
		return "<LoginForm('%s')>" % (self.email.data)


class RegistrationForm(Form):
	"""
		The new users registration form.
	"""
	username = TextField('Username', [validators.Length(min=4, max=25)])
	email = TextField('Email', [validators.Length(min=6, max=35)])
	password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')

	def __repr__(self):
		""" String representation of object. """
		return "<RegistrationForm('%s', '%s', '%s')>" % (self.name.data, self.fullname.data, self.email.data)