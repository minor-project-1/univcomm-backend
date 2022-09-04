from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456789@localhost/univcomm"
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()