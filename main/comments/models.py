from main.database import Base
from sqlalchemy import ForeignKey, Column, Boolean, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import functions


class Comment(Base):
    """ The post comment class. """
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    created = Column(DateTime, default=functions.current_timestamp())
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    approved = Column(Boolean, default=False)

    #post = relationship("Post") , backref=backref('comments',order_by=id))

    def __init__(self, content, user_id, post_id, approved=False):
        self.approved = approved
        self.content = content
        self.user_id = user_id
        self.post_id = post_id

    def __repr__(self):
        return "<Comment('%s', '%s')>" % (self.content, self.created)