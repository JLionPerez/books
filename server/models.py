from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey
Base = declarative_base()

class BookList(Base):
    __tablename__ = "book_list"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship("BookModel", back_populates="book_list", cascade="all, delete")

class BookModel(Base):
    __tablename__ = "book_model"

    id = Column(Integer(), primary_key = True)
    list_id = Column(Integer, ForeignKey("book_list.id"), nullable=False)
    google_books_id = Column(String())
    title = Column(String())
    author = Column(String())
    thumbnail = Column(String()) # url, points to img, not stored due to complexity and immense storage usage
    description = Column(Text())

    book_list = relationship("BookList", back_populates="books")