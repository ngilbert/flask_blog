from flask import Blueprint, request, session, g, redirect, url_for, \
        abort, render_template, flash, current_app
from flaskext.login import login_required, current_user
from models import Post, Comment
from forms import BlogPostForm, CommentForm
from jinja2 import TemplateNotFound

blog = Blueprint('blog', __name__, template_folder='templates')


@blog.route('/') 
def show_posts():
    """
        Show all blog posts.
    """
    current_app.logger.debug('Retrieving blog posts.')
    posts = g.db_session.query(Post).all()

    try:
        return render_template('index.html', posts=posts)
    except TemplateNotFound:
        abort(404)


@blog.route('/view/<int:post_id>')
def view_post(post_id):
    """
        View a post.
    """
    post = g.db_session.query(Post).filter_by(id=post_id).first()

    try:
        return render_template('view.html', post=post)
    except TemplateNotFound:
        abort(404)


@blog.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """
        Create a new blog post.
    """
    error = None 
    form = BlogPostForm(request.form)

    if request.method == 'POST' and form.validate():
        new_blog_post = Post(form.title.data, form.content.data, form.published.data, current_user.get_id())
        g.db_session.add(new_blog_post)
        flash('New Blog Post Created!')
        return redirect(url_for('blog.show_posts'))

    try:
        return render_template('new.html', form=form, error=error)
    except TemplateNotFound:
        abort(404)


@blog.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    """
        Edit a post.
    """
    post = g.db_session.query(Post).filter_by(id=post_id).first()
    form = BlogPostForm(request.form) 

    if request.method == 'POST' and form.validate():
        post = g.db_session.query(Post).filter_by(id=post_id).first()
        post.title = form.title.data
        post.content = form.content.data
        post.published = form.published.data
        return redirect(url_for('blog.show_posts'))

    form.title.data = post.title
    form.content.data = post.content
    form.published.data = post.published

    try:
        return render_template('edit.html', form=form, post=post)
    except TemplateNotFound:
        abort(404)


@blog.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    """
        Delete a blog post.
    """
    # TODO:  Implement delete.
    return redirect(url_for('admin'))


@blog.route('/comment/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comment(post_id):
    """
        Creates a comment for a blog post.

        GET - Displays comment form if user is logged in.
        POST - Writes comment to database.
    """
    form = CommentForm(request.form)
    post = g.db_session.query(Post).filter_by(id=post_id).first()

    if request.method == 'POST' and form.validate():
        comment = Comment()
        comment.content = form.content.data
        comment.post_id = post_id
        comment.user_id = current_user.get_id()

        g.db_session.add(comment)

        return redirect(url_for('blog.view', post_id=post_id))

    return render_template('comment.html', form=form, post=post)

