import os
import random

import requests

import movie_storage_sql as storage

OMDB_API_URL = "http://www.omdbapi.com/"


def get_valid_title():
    """Prompt the user for a non-empty movie title, or None to cancel."""
    while True:

        title = input("Enter Title (-1 to cancel): ").strip()

        if title == "-1":
            return None

        try:
            if title == "":
                raise ValueError
            return title
        except ValueError:
            print("Invalid title. Please enter a non-empty string.")


def get_valid_rating():
    """Prompt the user for a rating between 0 and 10, or None to cancel."""
    while True:

        rating = input("Enter rating (-1 to cancel): ")

        if rating == "-1":
            return None

        try:
            if float(rating) < 0 or float(rating) > 10:
                print("Rating must be between 0 and 10.")
                raise ValueError
            return float(rating)
        except ValueError:
            print("Invalid rating. Please enter a number.")


def fetch_movie_from_omdb(title):
    """Look up a movie by title on OMDb and return its data, or None if not found."""
    api_key = os.getenv("OMDB_API_KEY")
    if not api_key:
        print("Error: OMDB_API_KEY environment variable is not set.")
        return None

    try:
        response = requests.get(
            OMDB_API_URL,
            params={"apikey": api_key, "t": title},
            timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: could not reach OMDb API ({e}).")
        return None

    data = response.json()

    if data.get("Response") == "False":
        print(f"Error: {data.get('Error', 'movie not found.')}")
        return None

    return {
        "title": data.get("Title"),
        "year": int(data.get("Year", "0")[:4]),
        "rating": float(data.get("imdbRating", 0)) if data.get("imdbRating") != "N/A" else 0.0,
        "poster": data.get("Poster")
    }


def list_movies():
    """Display all movies, sorted by the option the user picks."""
    movies = storage.list_movies()

    sort_options = {
        "1": lambda items: sorted(
            items,
            key=lambda movie: movie[1]["rating"]
        ),
        "2": lambda items: sorted(
            items,
            key=lambda movie: movie[1]["rating"],
            reverse=True
        ),
        "3": lambda items: sorted(
            items,
            key=lambda movie: movie[1]["year"],
            reverse=True
        ),
        "4": lambda items: sorted(
            items,
            key=lambda movie: movie[1]["year"]
        ),
        "5": lambda items: sorted(
            items,
            key=lambda movie: movie[0]
        ),
        "6": lambda items: sorted(
            items,
            key=lambda movie: movie[0],
            reverse=True
        )
    }

    while True:
        print("\nList Movies")
        print("0. Back")
        print("1. Rating (lowest first)")
        print("2. Rating (highest first)")
        print("3. Year (latest first)")
        print("4. Year (oldest first)")
        print("5. Alphabetically (A-Z)")
        print("6. Alphabetically (Z-A)")

        choice = input("Choose an option: ")

        if choice == "0":
            return

        if choice not in sort_options:
            print("Invalid option.")
            continue

        sorted_movies = sort_options[choice](movies.items())
        print("\nMovies:")
        for title, details in sorted_movies:
            print(
                f"{title} "
                f"({details['year']}) "
                f"- Rating: {details['rating']}"
            )

        return


def add_movie():
    """Look up a movie on OMDb by title and add it to the database."""
    movies = storage.list_movies()

    title = get_valid_title()
    if title is None:
        return

    if title in movies:
        print(f"Movie '{title}' already exists.")
        return

    movie = fetch_movie_from_omdb(title)
    if movie is None:
        return

    storage.add_movie(movie["title"], movie["year"], movie["rating"], movie["poster"])


def delete_movie():
    """Delete a movie."""
    movies = storage.list_movies()

    title = get_valid_title()
    if title is None:
        return

    if title not in movies:
        print(f"Movie '{title}' not found.")
        return

    storage.delete_movie(title)


def update_movie():
    """Update a movie rating."""
    movies = storage.list_movies()

    title = get_valid_title()
    if title is None:
        return

    if title not in movies:
        print(f"Movie '{title}' not found.")
        return

    rating = get_valid_rating()
    if rating is None:
        return

    storage.update_movie(title, rating)


def movie_stats():
    """Calculate and print the average, median, best, and worst rated movie."""
    movies = storage.list_movies()
    print(movies)
    avg_rating = sum(movies[movie]["rating"] for movie in movies) / len(movies)
    print(f"Average rating: {avg_rating}")

    # median rating
    rating_list = sorted(movie["rating"] for movie in movies.values())
    if len(rating_list) % 2 == 1:
        median_rating = rating_list[len(rating_list) // 2]
    else:
        median_rating = (rating_list[len(rating_list) // 2] +
                         rating_list[len(rating_list) // 2 - 1]) / 2
    print(f"Median rating: {median_rating}")

    # max rating
    best_movie = max(movies.items(), key=lambda item: item[1]["rating"])
    print(f"Best movie: {best_movie[0]}, {best_movie[1]['rating']}")

    # min rating
    worst_movie = min(movies.items(), key=lambda item: item[1]["rating"])
    print(f"Worst movie: {worst_movie[0]}, {worst_movie[1]['rating']}")


def random_movie():
    """Pick and display a random movie from the database."""
    movies = storage.list_movies()
    movie = random.choice(list(movies.keys()))
    print(f"Your movie for tonight: {movie} ({movies[movie]["year"]}), it's rated {movies[movie]["rating"]}")


def search_movie():
    """Search for movies whose title contains the user's query."""
    movies = storage.list_movies()
    query = input("Enter part of movie name: ")
    for movie in movies:
        if query.lower() in movie.lower():
            print(f"{movie} ({movies[movie]["year"]}), {movies[movie]["rating"]}")


def movies_sorted_by_rating():
    """Sort the movies by rating in descending order and display them."""
    movies = storage.list_movies()
    movies_sorted = sorted(movies.items(), key=lambda item: item[1]["rating"], reverse=True)
    for title, info in movies_sorted:
        print(f"{title}: {info['rating']}")


def main_menu():
    """Print the menu, read the user's command, and dispatch to it in a loop."""
    print("Welcome to the Movie Database!")

    while True:
        print("\nMenu:")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5: Movie Stats")
        print("6: Random Movie")
        print("7: Search Movie")
        print("8: Movies Sorted By Rating")

        choice = input("Choose an option: ")

        if choice == "0":
            print("Bye!")
            break

        elif choice == "1":
            print("\nMovies:")
            list_movies()

        elif choice == "2":
            add_movie()

        elif choice == "3":
            delete_movie()

        elif choice == "4":
            update_movie()

        elif choice == "5":
            movie_stats()

        elif choice == "6":
            random_movie()

        elif choice == "7":
            search_movie()

        elif choice == "8":
            movies_sorted_by_rating()

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main_menu()