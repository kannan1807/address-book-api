"""Database engine, session factory, and declarative base."""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency: yields a DB session, always closes it."""
    db = SessionLocal()
    try:
        yield db
        logger.debug("DB session opened")
    finally:
        db.close()
        logger.debug("DB session closed")