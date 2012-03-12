from flask import g, current_app
from flaskext.login import LoginManager
from models import User, AuthUser, Anonymous

login_manager = LoginManager()

def init_login_manager(app):
	login_manager.login_view = 'users.login'
	login_manager.login_message = u"You must be logged in to view this page."
	login_manager.setup_app(app)


@login_manager.user_loader
def load_user(id):
    current_app.logger.debug('Loading user')
    user = g.db_session.query(User).filter_by(id=id).first()
    if user is not None:
        auth_user = AuthUser(user.id, user.username, user.role, user.confirmed)
        return auth_user

    return None 