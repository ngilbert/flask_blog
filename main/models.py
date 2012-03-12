from main.database import Base
from sqlalchemy import ForeignKey, Column, Boolean, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import functions



class Page(Base):
    """ The page class. """
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, name, content, user_id):
        self.name = name
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return "<Page('%s', '%s')>" % (self.name, self.content)
