from fastapi import FastAPI
from database import engine, Session
from models import Base, BookModel, BookList
from pydantic import BaseModel

Base.metadata.create_all(engine)

class List(BaseModel):
    name: str

class Book(BaseModel):
    list_id: int
    google_books_id: str
    title: str
    author: str
    thumbnail: str | None = None
    description: str | None = None
    
app = FastAPI()

# CRUD List




# CRUD Book

@app.post("/books")
async def create_book_in_list(book: Book):
    db = Session()
    new_book = BookModel(
        list_id=book.list_id,
        google_books_id=book.google_books_id, 
        title=book.title,
        author=book.author,
        thumbnail=book.thumbnail,
        description=book.description
    )
    db.add(new_book)
    db.commit()
    return new_book

@app.get("/books")
async def get_all_books_in_list():
    db = Session()
    books_query = db.query(BookModel)
    return books_query.all()

@app.get("/books/{id}")
async def get_book_in_list(id: int):
    db = Session()
    books_query = db.query(BookModel).filter(BookModel.id==id)
    book = books_query.first()
    return book

@app.delete("/books/{id}")
async def delete_book_in_list(id: int):
    db = Session()
    books_query = db.query(BookModel).filter(BookModel.id==id)
    book = books_query.first()
    db.delete(book)
    db.commit()
    return {"Deleted ": book.title}