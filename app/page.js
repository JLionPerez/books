"use client";
import { useState, useEffect } from "react";

export default function Home() {
  const key = "AIzaSyAAAc5MboaBXYWpD0mkYIPQfRNUDlGP43A"
  const [search, setSearch] = useState("")
  const url = `https://www.googleapis.com/books/v1/volumes?q=${search}&langRestrict=en&printType=books&key=${key}`
  const [books, setBooks] = useState([])

  const handleSearch = (event) => {
    setSearch(event.target.value)
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    useEffect(() => {
      const response = fetch(url)
      .then(response => response.json())
      .then(data => setBooks(data.items))
    },[])
  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        <label>
          Enter search terms:
          <input type="text" value={search} onChange={handleSearch}/>
        </label>
        <button type="submit">Search</button>
      </form>
      <div>{books.map(book => (
        <div key={book.id}>
          <img src={book.volumeInfo.imageLinks.thumbnail}></img>
          <p id="name">{book.volumeInfo.title} by {book.volumeInfo.authors}</p>
          <p id="text">{book.volumeInfo.description}</p>
        </div>
      ))}</div>
    </>
  );
}

