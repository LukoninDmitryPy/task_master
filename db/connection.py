from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import scoped_session, sessionmaker

from config import PG, ECHO_DB


url_object = URL.create(
    PG['driv'],
    username=PG['user'],
    password=PG['pass'],
    host=PG['host'],
    database=PG['name'],
    port=PG['port']
)

engine = create_engine(url_object, pool_recycle=3600, echo=ECHO_DB, pool_pre_ping=True)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
Session.expire_on_commit = False

def dbconnect(func):
    def inner(*args, **kwargs):
        session = Session()  # (this is now a scoped session)
        try:
            return func(*args, **kwargs) # No need to pass session explicitly
        except:
            session.rollback()

            session = Session()
            return func(*args, **kwargs)
        finally:
            session.expunge_all()
            session.commit()
            session.close()  # NOTE: *remove* rather than *close* here
    return inner