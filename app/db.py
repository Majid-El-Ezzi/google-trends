import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db_url= os.getenv("DATABASE_URL", "postgresql+psycopg2://majid:majid@localhost:5432/trends")

engine = create_engine(db_url)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)