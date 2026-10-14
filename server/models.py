from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table

Base = declarative_base()

book_list_link = Table(
    "book_list_link",
    Base.metadata,
    Column("list_id", Integer, ForeignKey("book_list.id", ondelete="CASCADE"), primary_key=True),
    Column("book_id", Integer, ForeignKey("book_model.id", ondelete="CASCADE"), primary_key=True),
)

class BookList(Base):
    __tablename__ = "book_list"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    books = relationship("BookModel", secondary=book_list_link, back_populates="lists")

class BookModel(Base):
    __tablename__ = "book_model"

    id = Column(Integer(), primary_key = True)
    google_books_id = Column(String(), unique=True)
    title = Column(String())
    author = Column(String())
    thumbnail = Column(String()) # url, points to img, not stored due to complexity and immense storage usage
    description = Column(Text())

    lists = relationship("BookList", secondary=book_list_link, back_populates="books")