from flask import Blueprint, request, g, redirect, url_for, \
        abort, render_template, flash
from jinja2 import TemplateNotFound
from flaskext.login import login_required, current_user
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
        return render_template('comment.html', form=form, post=post)
    except TemplateNotFound:
        abort(404)
