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



