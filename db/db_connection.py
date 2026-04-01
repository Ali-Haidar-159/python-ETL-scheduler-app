import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

load_dotenv() 

db_url = os.getenv("DB_URL")


def get_connection():
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine

Session = sessionmaker(bind=get_connection())
