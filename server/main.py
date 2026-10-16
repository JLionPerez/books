from fastapi import FastAPI, HTTPException, Depends
from database import engine, Session
from models import Base, BookModel, BookList
from pydantic import BaseModel

Base.metadata.create_all(engine)

class List(BaseModel):
    name: str

class Book(BaseModel):
    google_books_id: str
    title: str
    author: str
    thumbnail: str | None = None
    description: str | None = None
    
app = FastAPI()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# CRUD List

@app.post("/lists")
async def create_list(l: List, db = Depends(get_db)):
    new_list = db.query(BookList).filter(BookList.name == l.name).first()

    if new_list is not None:
        raise HTTPException(status_code=400, detail="List already exists")
    
    new_list = BookList(name=l.name)
    db.add(new_list)

    db.commit()
    return new_list

# CRUD Book

@app.post("/lists/{list_id}/books")
async def create_book_in_list(list_id: int, book: Book, db = Depends(get_db)):
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
    else:
        raise HTTPException(status_code=400, detail="Book already in list")
    
    db.commit()
    return new_book

@app.get("/lists/{list_id}/books")
async def get_all_books_in_list(list_id: int, db = Depends(get_db)):
    book_list = db.query(BookList).filter(BookList.id == list_id).first()
    
    if book_list is None:
        raise HTTPException(status_code=404, detail="List not found")
    
    return book_list.books

@app.get("/lists/{list_id}/books/{book_id}")
async def get_book_in_list(list_id: int, book_id: int, db = Depends(get_db)):
    book = db.query(BookModel).filter(
        BookModel.id == book_id,
        BookModel.lists.any(BookList.id == list_id)
    ).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book

# @app.put("/lists/{list_id}/books/")

@app.delete("/lists/{list_id}/books/{book_id}")
async def delete_book_in_list(list_id: int, book_id: int, db = Depends(get_db)):
    book_list = db.query(BookList).filter(BookList.id==list_id).first()
    book = db.query(BookModel).filter(
        BookModel.id == book_id,
        BookModel.lists.any(BookList.id == list_id)
    ).first()
    
    if book_list is None:
        raise HTTPException(status_code=404, detail="List not found")
    if book not in book_list.books:
        raise HTTPException(status_code=404, detail="Book not in this list")
    
    book_list.books.remove(book)

    if not book.lists:
        db.delete(book)
    
    db.commit()
    return {"Deleted ": book.title}