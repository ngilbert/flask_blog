from main.database import Base
from sqlalchemy import ForeignKey, Column, Boolean, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import functions


class Post(Base):
    """ The post class. """
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    published = Column(Boolean, default=False)
    created = Column(DateTime, default=functions.current_timestamp())
    user_id =  Column(Integer, ForeignKey('users.id'))

    comments = relationship("Comment", order_by="Comment.id", backref="post")

    def __init__(self, title, content, published, user_id):
        self.title = title
        self.content = content
        self.published = published
        self.user_id = user_id

    def __repr__(self):
        return "<Post('%s', '%s', '%s', '%s')>" % (self.title, self.content, self.published, self.created)


class Comment(Base):
    """ The post comment class. """
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    created = Column(DateTime, default=functions.current_timestamp())
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    def __init__(self, content, user_id, post_id):
        self.content = content
        self.user_id = user_id
        self.post_id = post_id

    def __repr__(self):
        return "<Comment('%s', '%s')>" % (self.content, self.created)