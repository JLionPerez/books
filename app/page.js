"use client";
import { useState, useEffect } from "react";

export default function Home() {
  const key = "AIzaSyAAAc5MboaBXYWpD0mkYIPQfRNUDlGP43A"
  const [search, setSearch] = useState("")
  const [books, setBooks] = useState([])

  const handleSearch = (event) => {
    setSearch(event.target.value)
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    const url = `https://www.googleapis.com/books/v1/volumes?q=${search}&langRestrict=en&printType=books&key=${key}`
    const response = fetch(url)
    .then(response => response.json())
    .then(data => setBooks(data.items))
    .catch(error => {
      console.error('Error fetch data: ', error)
    })
  }

  return (
      <div className="container">
        <div className="header">
          <div className="hero">
            <h1>Book Search</h1>
            <p>Use the Google Books API to search through their libraries.</p>
            <p>*Currently work in progress.*</p>
          </div>
          <form onSubmit={handleSubmit}>
            <input type="text" value={search} onChange={handleSearch} placeholder=""/>
            <button type="submit">Search Books</button>
            <img className="search_logo" src="/poweredby.png"></img>
          </form>
        </div>
        <div className="library">{books.map(book => (
          <div className="book" key={book.id}>
            <img className="thumbnail" src={book.volumeInfo.imageLinks.thumbnail}></img>
            <div className="description">
              <h3 id="name">{book.volumeInfo.title} by {book.volumeInfo.authors}</h3>
              <p id="text">{book.volumeInfo.description}</p>
            </div>
          </div>
        ))}</div>
      </div>
  );
}

