from fastapi import FastAPI
from database import engine, Session
from models import Base, Favorite
from pydantic import BaseModel

Base.metadata.create_all(engine)

class Book(BaseModel):
    google_books_id: str
    title: str
    author: str
    thumbnail: str | None = None
    description: str | None = None
    
app = FastAPI()

@app.post("/favorites")
async def create_favorite(book: Book):
    db = Session()
    new_favorite = Favorite(
        google_books_id=book.google_books_id, 
        title=book.title,
        author=book.author,
        thumbnail=book.thumbnail,
        description=book.description
    )
    db.add(new_favorite)
    db.commit()
    return new_favorite

@app.get("/favorites")
async def get_all_favorites():
    db = Session()
    favorites_query = db.query(Favorite)
    return favorites_query.all()

@app.get("/favorites/{id}")
async def get_favorite_book(id: int):
    db = Session()
    favorites_query = db.query(Favorite).filter(Favorite.id==id)
    favorite = favorites_query.first()
    return favorite

@app.delete("/favorites/{id}")
async def delete_favorite_book(id: int):
    db = Session()
    favorites_query = db.query(Favorite).filter(Favorite.id==id)
    favorite = favorites_query.first()
    db.delete(favorite)
    db.commit()
    return {"Deleted ": favorite.title}