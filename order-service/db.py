from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Change this variable name to SQLALCHEMY_DATABASE_URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:cooper@postgres-service:5432/byteburst_catalog"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()