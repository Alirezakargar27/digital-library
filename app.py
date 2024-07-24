from flask import Flask, render_template, request, redirect, url_for, flash
from data_models import db, Author, Book
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Set the database URI using an absolute path
db_path = os.path.join(os.path.abspath(os.getcwd()), 'data/library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database connection with the app
db.init_app(app)


def seed_data():
    # Check if data already exists to avoid duplicate entries
    if Author.query.count() == 0 and Book.query.count() == 0:
        authors = [
            Author(name="J.K. Rowling", birth_date=datetime.strptime("1965-07-31", "%Y-%m-%d").date()),
            Author(name="George R.R. Martin", birth_date=datetime.strptime("1948-09-20", "%Y-%m-%d").date()),
            Author(name="J.R.R. Tolkien", birth_date=datetime.strptime("1892-01-03", "%Y-%m-%d").date(),
                   date_of_death=datetime.strptime("1973-09-02", "%Y-%m-%d").date()),
            Author(name="Agatha Christie", birth_date=datetime.strptime("1890-09-15", "%Y-%m-%d").date(),
                   date_of_death=datetime.strptime("1976-01-12", "%Y-%m-%d").date()),
            Author(name="Mark Twain", birth_date=datetime.strptime("1835-11-30", "%Y-%m-%d").date(),
                   date_of_death=datetime.strptime("1910-04-21", "%Y-%m-%d").date())
        ]
        for author in authors:
            db.session.add(author)

        db.session.commit()

        books = [
            Book(isbn="9780747532743", title="Harry Potter and the Philosopher's Stone", publication_year=1997,
                 author_id=authors[0].id),
            Book(isbn="9780553103540", title="A Game of Thrones", publication_year=1996, author_id=authors[1].id),
            Book(isbn="9780261103573", title="The Lord of the Rings", publication_year=1954, author_id=authors[2].id),
            Book(isbn="9780007136834", title="Murder on the Orient Express", publication_year=1934,
                 author_id=authors[3].id),
            Book(isbn="9780486280615", title="Adventures of Huckleberry Finn", publication_year=1884,
                 author_id=authors[4].id)
        ]
        for book in books:
            db.session.add(book)

        db.session.commit()


# Create the tables and seed data
with app.app_context():
    seed_data()  # Seed the data


@app.route('/')
def home():
    sort_by = request.args.get('sort_by', 'title')
    keyword = request.args.get('keyword', '')

    query = Book.query

    if keyword:
        query = query.filter(Book.title.ilike(f'%{keyword}%'))

    if sort_by == 'author':
        query = query.join(Author).order_by(Author.name)
    else:
        query = query.order_by(Book.title)

    books = query.all()

    return render_template('home.html', books=books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = datetime.strptime(request.form['birthdate'], "%Y-%m-%d").date()
        date_of_death = request.form['date_of_death']
        if date_of_death:
            date_of_death = datetime.strptime(date_of_death, "%Y-%m-%d").date()
        else:
            date_of_death = None
        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()
        flash('Author added successfully!')
        return redirect(url_for('add_author'))
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    authors = Author.query.all()
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']
        new_book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!')
        return redirect(url_for('add_book'))
    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    author_id = book.author_id

    db.session.delete(book)
    db.session.commit()

    # Check if the author has any other books
    author_books = Book.query.filter_by(author_id=author_id).count()
    if author_books == 0:
        author = Author.query.get(author_id)
        db.session.delete(author)
        db.session.commit()

    flash('Book and author (if no other books) deleted successfully!')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
