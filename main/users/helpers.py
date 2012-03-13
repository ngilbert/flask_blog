from flask import flash, redirect, url_for
from flaskext.login import current_user
from functools import wraps
import constants as USER
import hashlib


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

def access_level_required(requested_access_level):
    def wrap(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            if current_user.role <= requested_access_level:
                    return func(*args, **kwargs)
            else:
                flash('Access denied.')
                return redirect(url_for('index'))
        return decorated_func
    return wrap