from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy.exc import IntegrityError
from models import db, Movie, Blog
from helpers import get_movies, get_blogs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ANAGOGIDZE'  # Ensure this key is unique and secure
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # SQLite URI
db.init_app(app)

#https://medium.com/@nithinbharathwaj/sqlalchemy-with-python-flask-089ba97c4612

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/movies')
def movies():
    search_query = request.args.get('search')
    if search_query:
        all_movies = Movie.query.filter(Movie.title.contains(search_query)).order_by(Movie.id.desc()).all()
    else:
        all_movies = Movie.query.order_by(Movie.id.desc()).all()
    return render_template("movies.html", movies=all_movies, search_query=search_query)

@app.route('/add/movie', methods=['GET', 'POST'])
def addMovie():
    if request.method == 'POST':
        # Process the form data
        title = request.form['title'].strip()
        genre = request.form['genre'].strip()
        desc = request.form['desc'].strip()
        image = request.form['image'].strip()

        # Create a new movie instance
        new_movie = Movie(
            title=title,
            genre=genre,
            desc=desc,
            image=image
        )

        # Add and commit to the database
        try:
            db.session.add(new_movie)
            db.session.commit()
            flash('ფილმი წარმატებით დაემატა!', 'success')
            return redirect(url_for('addMovie'))
        except IntegrityError:
            db.session.rollback()
            flash('შეცდომა!: აღნიშნული ფილმი უკვე არსებობს.', 'danger')


    return render_template("add_movie.html")

@app.route('/movies/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template("movie_detail.html", movie=movie)

@app.route('/insert-movies')
def insertMovies():
    url = "https://srulad.com"
    for page in range(1, 3):
        get_movies(url, page)
    return redirect(url_for('movies'))


@app.route('/blogs')
def blogs():
    search_query = request.args.get('search')
    if search_query:
        all_blogs = Blog.query.filter(Blog.title.contains(search_query)).order_by(Blog.id.desc()).all()
    else:
        all_blogs = Blog.query.order_by(Blog.id.desc()).all()

    return render_template("blogs.html", blogs=all_blogs, search_query=search_query)


@app.route('/add/blog', methods=['GET', 'POST'])
def addBlog():
    if request.method == 'POST':
        # Process the form data
        title = request.form['title'].strip()
        desc = request.form['desc'].strip()
        image = request.form['image'].strip()

        # Create a new movie instance
        new_blog = Blog(
            title=title,
            desc=desc,
            image=image
        )

        # Add and commit to the database
        try:
            db.session.add(new_blog)
            db.session.commit()
            flash('ბლოგი წარმატებით დაემატა!', 'success')
            return redirect(url_for('addBlog'))
        except IntegrityError:
            db.session.rollback()
            flash('შეცდომა!: აღნიშნული ბლოგი უკვე არსებობს.', 'danger')


    return render_template("add_blog.html")

@app.route('/blogs/<int:blog_id>')
def blog_detail(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    return render_template("blog_detail.html", blog=blog)



@app.route('/insert-blogs')
def insertBlogs():
    url = "https://srulad.com"
    for page in range(1, 3):
        get_blogs(url, page)
    return redirect(url_for('blogs'))



if __name__ == '__main__':
   app.run(debug = True)