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
