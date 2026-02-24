"use client";
import { useState, useEffect } from "react";

export default function Home() {
  const key = "AIzaSyAAAc5MboaBXYWpD0mkYIPQfRNUDlGP43A"
  const url = `https://www.googleapis.com/books/v1/volumes?q=all&printType=books&key=${key}`
  const [books, setBooks] = useState([])

  useEffect(() => {
    const response = fetch(url)
    .then(response => response.json())
    .then(data => setBooks(data.items)) //console.log(data)
  },[])

  return (
    <>
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

