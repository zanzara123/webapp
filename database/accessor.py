from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from settings import Settings

settings = Settings()

engine = create_engine(settings.db_url)

session_factory = sessionmaker(engine)

def get_db_session() -> sessionmaker[Session]:
    return session_factory

