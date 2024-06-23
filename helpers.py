import requests
from bs4 import BeautifulSoup
from models import db, Movie, Blog  # Import from models.py
from flask import current_app

def get_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def get_description(url):
    soup = get_html(url)
    if soup:
        return soup.find(class_="plot").text.strip()
    return ""

def get_movies(url, page):
    soup = get_html(f"{url}/movies/page/{page}")
    if soup:
        # Target the search_result section
        search_result_section = soup.find(id="search_result")
        if not search_result_section:
            return "No Result"

        elements = search_result_section.find_all(class_='movie-item')
        for element in elements:
            title = element.find(class_="card-title").text.strip()
            image = element.find(class_="card-img-top")['src']
            genre = element.find(class_="card-genre").text.strip()
            link = element.find(class_='view-more')['href']
            link = f"{url}/{link}"
            desc = get_description(link)


            movies = {'title': title, 'image': image, 'genre': genre, 'desc': desc}
            save_movie(movies)


def get_blogs(url, page):
    soup = get_html(f"{url}/blog/page/{page}")
    if soup:

        search_result_section = soup.find(id="search_result")
        if not search_result_section:
            return "No Result"

        # Adjust this based on actual HTML structure
        elements = search_result_section.find_all(class_='card')  # Adjust selector
        for element in elements:
            title = element.find(class_="card-title").text.strip()
            image = element.find(class_="card-img-top")['src']
            image = f"{url}{image}"
            link = element.find(class_='view-more')['href']  # Movie link
            link = f"{url}/{link}"
            desc = get_description(link)

            blogs = {'title': title, 'image': image, 'desc': desc}
            save_blog(blogs)

def save_movie(movie_data):
    with current_app.app_context():
        existing_movie = Movie.query.filter_by(desc=movie_data['desc']).first()
        if existing_movie is None:
            movie = Movie(
                title=movie_data['title'],
                image=movie_data['image'],
                genre=movie_data['genre'],
                desc=movie_data['desc']
            )
            db.session.add(movie)
            db.session.commit()
        else:
            print(f"Movie '{movie_data['title']}' already exists in the database.")


def save_blog(blog_data):
    with current_app.app_context():
        if not Blog.query.filter_by(title=blog_data['title']).first():
            blog = Blog(
                title=blog_data['title'],
                image=blog_data['image'],
                desc=blog_data['desc']
            )
            db.session.add(blog)
            db.session.commit()
        else:
            print(f"Blog '{blog_data['title']}' already exists in the database.")