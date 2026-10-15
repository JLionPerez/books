from fastapi import FastAPI, HTTPException
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

@app.post("/lists/{list_id}/books")
async def create_book_in_list(list_id: int, book: Book):
    db = Session()
    book_list = db.query(BookList).filter(BookList.id == list_id).first()
    if book_list is None:
        raise HTTPException(status_code=404, detail="List not found")
    
    new_book = db.query(BookModel).filter(BookModel.google_books_id == book.google_books_id).first()
    if new_book is None:
        new_book = BookModel(
                google_books_id=book.google_books_id, 
                title=book.title,
                author=book.author,
                thumbnail=book.thumbnail,
                description=book.description
            )
        db.add(new_book)

    if new_book not in book_list.books:
        book_list.books.append(new_book)
    
    db.commit()
    return new_book

@app.get("/lists/{list_id}/books")
async def get_all_books_in_list(list_id: int):
    db = Session()
    book_list = db.query(BookList).filter(BookList.id == list_id).first()
    
    if book_list is None:
        raise HTTPException(status_code=404, detail="List not found")
    
    return book_list.books

@app.get("/lists/{list_id}/books/{book_id}")
async def get_book_in_list(list_id: int, book_id: int):
    db = Session()
    book = db.query(BookModel).filter(
        BookModel.id == book_id,
        BookModel.lists.any(BookList.id == list_id)
    ).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book

@app.delete("/lists/{list_id}/books/{book_id}")
async def delete_book_in_list(list_id: int, book_id: int):
    db = Session()
    book_list = db.query(BookList).filter(BookList.id==list_id).first()
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    
    if book_list is None:
        raise HTTPException(status_code=404, detail="List not found")
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book_list.books.remove(book)

    if not book.lists:
        db.delete(book)
    
    db.commit()
    return {"Deleted ": book.title}