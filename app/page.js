"use client";
import { useState } from "react";

export default function Home() {
  const key = process.env.NEXT_PUBLIC_API_KEY;
  const [search, setSearch] = useState("")
  const [books, setBooks] = useState([])
  const inputMessage = ""

  const handleSearch = (event) => {
    setSearch(event.target.value)
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    if(!search) {
      alert('Please enter a search term.')
    } else {
      const url = `https://www.googleapis.com/books/v1/volumes?q=${search}&langRestrict=en&printType=books&key=${key}`
      fetch(url)
      .then(response => response.json())
      .then(data => {
        if (!data.totalItems) {
          alert('That book does not exist.')
        } else {
          console.log("totalItems: ", data.totalItems)
          setBooks(data.items)
        }
      })
      .catch(error => {
        console.error('Error fetch data: ', error)
      })
    }
  }

  return (
      <div className="container">
        <div className="header">
          <div className="hero">
            <h1>Book Search</h1>
            <p>Use the Google Books API to search through their libraries.</p>
          </div>
          <form onSubmit={handleSubmit}>
            <input type="text" value={search} onChange={handleSearch} placeholder=""/>
            <button type="submit">Search Books</button>
            <img className="search_logo" src="/poweredby.png"></img>
          </form>
        </div>
        <div className="library">{books.map(book => (
          <div className="book" key={book.id}>
            <img className="thumbnail" src={book.volumeInfo.imageLinks?.thumbnail}></img>
            <div className="description">
              <h3 id="name">{book.volumeInfo.title} by {book.volumeInfo.authors}</h3>
              <p id="text">{book.volumeInfo.description}</p>
            </div>
          </div>
        ))}</div>
      </div>
  );
}

