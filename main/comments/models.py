from main.database import Base
from sqlalchemy import ForeignKey, Column, Boolean, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import functions


class Comment(Base):
    """ The post comment class. """
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    created = Column(DateTime, default=functions.current_timestamp())
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    published = Column(Boolean, default=False)

    def __init__(self, content, user_id, post_id):
        self.content = content
        self.user_id = user_id
        self.post_id = post_id

    def __repr__(self):
        return "<Comment('%s', '%s')>" % (self.content, self.created)