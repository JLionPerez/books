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
async def create_item(book: Book):
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