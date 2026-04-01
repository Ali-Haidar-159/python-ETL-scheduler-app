from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Photos(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    url = Column(String(255))
