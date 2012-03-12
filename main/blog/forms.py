from wtforms import Form, BooleanField, TextField, TextAreaField, validators


class BlogPostForm(Form):
    """
        The blog post creation form.
    """
    title = TextField('Title', [validators.Required()])
    content = TextAreaField('Content', [validators.Required()])
    published = BooleanField('Published', [validators.Required()])

    def __repr__(self):
        """ String representation of object. """
        return "<BlogPost('%s', '%s', '%s')>" % (self.title.data, self.content.data, self.published.data)


class CommentForm(Form):
    """
        The comment form.
    """
    content = TextAreaField('Content', [validators.Required()])

    def __repr__(self):
        """ String representation of object. """
        return "<CommentForm('%s')>" % (self.content.data)


if __name__ == "__main__":
    form = BlogPostForm()
    form.title.data = 'Test Title'
    form.content.data = 'Test content'
    form.published.data = False
    print 'title = ' + form.title.data 
    print 'content = ' + form.content.data
    print 'valid = ' + str(form.validate())
