from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Book Search APU is running"}