import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from vrs_analytics.core.base import Base
from vrs_analytics.db.postgres import models 

load_dotenv() 

db_user     = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name     = os.getenv("DB_NAME")
db_driver   = "postgresql+psycopg2"  
db_host     = "localhost"
db_port     = 5432

connection_url = URL.create(
    drivername=db_driver,
    username=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
    database=db_name
)


def get_connection():
    engine = create_engine(connection_url)
    Base.metadata.create_all(engine)
    return engine

Session = sessionmaker(bind=get_connection())
