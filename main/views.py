from flask import Blueprint, Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
from . import app


""" ---------------------------------------------------------------------------
	F U N C T I O N S
--------------------------------------------------------------------------- """
@app.route('/')
def index():
    return redirect(url_for('blog.show_posts'))

