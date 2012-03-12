from flask import Flask, g
from database import db_session
import config
from blog.views import blog
from admin.views import admin
from users.views import users

app = Flask(__name__)

app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(blog, url_prefix='/blog')
app.register_blueprint(admin, url_prefix='/admin')

app.secret_key = config.SECRET_KEY
app.debug = config.DEBUG


#TODO:  Some stuff.
@app.before_request
def before_request():
    """
        Perform any setup before handling the request.
    """
    g.db_session = db_session


@app.teardown_request
def shutdown_session(exception=None):
    """
        Handle any clean up that needs to occur after the request has been handled.
            - Commit sqlalchemy session to database.
    """
   # Check that no errors occurred and that there are changes to commit.
    if exception is None:
        g.db_session.commit()
    # Dispose of the current contextual session.
    g.db_session.remove()


import users
users.init_login_manager(app)
import views
import blog.views
import admin.views
import users.views
