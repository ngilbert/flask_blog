from main.database import Base
from flaskext.login import UserMixin, AnonymousUser
from sqlalchemy import Column, SmallInteger, Integer, String, Boolean


class Anonymous(AnonymousUser):
	name = u"Anonymous"


class AuthUser(UserMixin):
	""" The user class used by flaskext.login. """
	def __init__(self, id, username, role, confirmed=False, active=True):
		self.id = id
		self.username = username
		self.role = role
		self.confirmed = confirmed
		self.active = active

	def is_active(self):
		return self.active


class User(Base):
	""" The user class. """
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	username = Column(String(50), unique=True)
	email = Column(String(256), unique=True)
	password = Column(String(1024))
	role = Column(SmallInteger)
	confirmation_key = Column(String(64))
	confirmed = Column(Boolean)
	reset_key = Column(String(65))

	def __init__(self, username, email, password, role, confirmation_key, confirmed=False, reset_key=None):
		self.username = username
		self.email = email
		self.password = password
		self.role = role
		self.confirmation_key = confirmation_key
		self.confirmed = confirmed
		self.reset_key = reset_key

	def __repr__(self):
		return "<User('%s', '%s', '%s')>" % (self.username, self.email, self.role)