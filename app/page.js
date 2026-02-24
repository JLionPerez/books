"use client";
import styles from "./page.module.css";
import { useState, useEffect } from "react";

export default function Home() {
  const key = "AIzaSyAAAc5MboaBXYWpD0mkYIPQfRNUDlGP43A"
  const url = `https://www.googleapis.com/books/v1/volumes?q=intitle:flowers+inauthor:keyes&key=${key}`
  const [books, setBooks] = useState([])

  useEffect(() => {
    const response = fetch(url).then(response => response.json()).then(data => setBooks(data.items));
    // console.log(books)
  },[])

  return (
    <>
      <div>{books.map(book => (
        <div key={book.id}>
          {book.volumeInfo.title} by {book.volumeInfo.authors}
        </div>
      ))}</div>
    </>
  );
}

