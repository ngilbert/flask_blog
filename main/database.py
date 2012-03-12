from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_CONNECTION_STRING, SECRET_KEY
#from users.models import User
#from blog.models import Post
#from comments.models import Comment


engine = create_engine(DATABASE_CONNECTION_STRING, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()


def init_db():
    """
        Initialize the database for the first time.
    """
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
