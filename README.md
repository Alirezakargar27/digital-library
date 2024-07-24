# Digital Library

## Description

Digital Library is a web-based application built using Flask that allows users to manage a collection of books and authors. The application provides features to add new authors and books, search for books by title, and delete books along with their associated authors if they have no other books.

## Features

- **Add Authors**: Add details such as name, birthdate, and date of death for authors.
- **Add Books**: Add details such as ISBN, title, publication year, and author for books.
- **Search Books**: Search for books by title using a search form.
- **Delete Books**: Delete books from the library and remove the author if they have no other books.

## Tools, Technologies, Libraries, and Concepts Used

- **Python**: The primary programming language used.
- **Flask**: The web framework used to build the application.
- **Flask-SQLAlchemy**: Used for ORM (Object Relational Mapping) to interact with the SQLite database.
- **SQLite**: The database used to store information about authors and books.
- **HTML/CSS**: For creating the frontend templates.
- **Jinja2**: Templating engine used with Flask to render HTML.
- **WTForms**: For creating and validating forms.
- **Git**: Version control system.
- **GitHub**: Hosting the project repository.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/alirezakargar27/new-digital-library.git
   cd new-digital-library
