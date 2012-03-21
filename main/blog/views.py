from flask import Blueprint, request, session, g, redirect, url_for, \
        abort, render_template, flash 
from jinja2 import TemplateNotFound
from flaskext.login import login_required, current_user
from main.users import constants as USER
from main.users.helpers import access_level_required
from models import Post
from forms import BlogPostForm 


blog = Blueprint('blog', __name__, template_folder='templates')


@blog.route('/') 
def show_posts():
    """
        Show all blog posts.
    """
    posts = g.db_session.query(Post).all()

    try:
        return render_template('blog_index.html', posts=posts)
    except TemplateNotFound:
        abort(404)


@blog.route('/view/<int:post_id>')
def view_post(post_id):
    """
        View a post.
    """
    post = g.db_session.query(Post).filter_by(id=post_id).first()

    try:
        return render_template('blog_view.html', post=post)
    except TemplateNotFound:
        abort(404)


@blog.route('/manage', methods=['GET'])
@login_required
@access_level_required(USER.ADMIN)
def manage():
    """
        Manage blog posts.
    """
    unpublished_posts = g.db_session.query(Post).filter_by(published=False).all()
    published_posts = g.db_session.query(Post).filter_by(published=True).all()

    try:
        return render_template('blog_manage.html', published_posts=published_posts, unpublished_posts=unpublished_posts)
    except TemplateNotFound:
        abort(404)


@blog.route('/publish', methods=['GET'])
@login_required
@access_level_required(USER.ADMIN)
def publish(post_id):
    """
        Mark a post as published.
    """
    post = g.db_session.query(Post).filter_by(id=post_id).first()
    post.published = True

    flash('Blog post published')
    return redirect(url_for('blog.manage'))


@blog.route('/new', methods=['GET', 'POST'])
@login_required
@access_level_required(USER.ADMIN)
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
        return render_template('blog_new.html', form=form, error=error)
    except TemplateNotFound:
        abort(404)


@blog.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
@access_level_required(USER.ADMIN)
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
        return render_template('blog_edit.html', form=form, post=post)
    except TemplateNotFound:
        abort(404)


@blog.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
@access_level_required(USER.ADMIN)
def delete(post_id):
    """
        Delete a blog post.
    """
    # TODO:  Implement delete.
    return redirect(url_for('admin'))

