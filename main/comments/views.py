from flask import Blueprint, request, g, redirect, url_for, \
        abort, render_template, flash
from jinja2 import TemplateNotFound
from flaskext.login import login_required, current_user
from main.users import constants as USER
from main.users.helpers import access_level_required
from main.blog.models import Post
from models import Comment
from forms import CommentForm

comments = Blueprint('comments', __name__, template_folder='templates')


@comments.route('/comments/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comment(post_id=None):
    """
        Creates a comment for a blog post.

        GET - Displays comment form if user is logged in.
        POST - Writes comment to database.
    """
    form = CommentForm(request.form)
    post = g.db_session.query(Post).filter_by(id=post_id).first()

    if request.method == 'POST' and form.validate():
        comment = Comment(form.content.data, current_user.get_id(), post.id)
        g.db_session.add(comment)

        return redirect(url_for('blog.view_post', post_id=post_id))

    try:
        return render_template('comment_new.html', form=form, post=post)
    except TemplateNotFound:
        abort(404)


@comments.route('/manage', methods=['GET'])
@login_required
@access_level_required(USER.ADMIN)
def manage():
    """
        Manage user comments.
    """
    comments = g.db_session.query(Comment).filter_by(approved=False).all()

    try:
        return render_template('comments_manage.html', comments=comments)
    except TemplateNotFound:
        abort(404)


@comments.route('/approve/<int:comment_id>', methods=['GET'])
@login_required
@access_level_required(USER.ADMIN)
def approve(comment_id):
    """
        Approve a comment.
    """
    comment = g.db_session.query(Comment).filter_by(id=comment_id).first()
    comment.approved = True

    flash('Comment approved')
    return redirect(url_for('comments.manage'))


@comments.route('/delete/<int:comment_id>', methods=['GET'])
@login_required
@access_level_required(USER.ADMIN)
def delete(comment_id):
    """
        Delete a comment.
    """
    comment = g.db_session.query(Comment).filter_by(id=comment_id).first()
    g.db_session.delete(comment)

    flash('Comment deleted')
    return redirect(url_for('comments.manage'))

