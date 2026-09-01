from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

#postgresql+psycopg2://user:password@hostname/database_name
engine = create_engine("postgresql+psycopg2://postgres:pass@localhost:5432/pomodoro")

session_factory = sessionmaker(engine)

def get_db_session() -> sessionmaker[Session]:
    return session_factory
