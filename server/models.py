from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text
Base = declarative_base()

class Favorite(Base):
    __tablename__ = "favorite"

    id = Column(Integer(), primary_key = True)
    title = Column(String())
    author = Column(String())
    thumbnail = Column(String()) # url, points to img, not stored due to complexity and immense storage usage
    description = Column(Text())