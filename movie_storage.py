import json

MOVIES_FILE = "movies.json"


def get_movies():
    """
    Returns a dictionary of movies.

    Example:
    {
        "Titanic": {
            "rating": 9,
            "year": 1999
        }
    }
    """
    with open(MOVIES_FILE, "r") as file:
        return json.load(file)


def save_movies(movies):
    """
    Saves all movies to the JSON file.
    """
    with open(MOVIES_FILE, "w") as file:
        json.dump(movies, file, indent=4)


def add_movie(title, year, rating):
    """
    Adds a movie to the database.
    """
    movies = get_movies()

    movies[title] = {
        "rating": rating,
        "year": year
    }

    save_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the database.
    """
    movies = get_movies()

    if title in movies:
        del movies[title]

    save_movies(movies)


def update_movie(title, rating):
    """
    Updates a movie rating.
    """
    movies = get_movies()

    if title in movies:
        movies[title]["rating"] = rating

    save_movies(movies)