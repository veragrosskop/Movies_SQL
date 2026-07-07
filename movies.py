import random

import movie_storage


def get_valid_title():
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


def get_valid_year():
    while True:

        year = input("Enter year (-1 to cancel): ")

        if year == "-1":
            return None

        try:
            if int(year) < 0 or int(year) > 2026:
                raise ValueError
            return int(year)
        except ValueError:
            print("Invalid rating. Please enter a number.")


def get_valid_rating():
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


def list_movies():
    movies = movie_storage.get_movies()

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
    """
    Adds a movie.
    """
    movies = movie_storage.get_movies()

    title = get_valid_title()
    if title is None:
        return

    if title in movies:
        print(f"Movie '{title}' already exists.")
        return

    year = get_valid_year()
    if year is None:
        return

    rating = get_valid_rating()
    if rating is None:
        return

    movie_storage.add_movie(title, year, rating)

    print(
        f"Movie '{title}' from {year} "
        f"with rating {rating} added successfully."
    )


def delete_movie():
    """
    Deletes a movie.
    """
    movies = movie_storage.get_movies()

    title = get_valid_title()
    if title is None:
        return

    if title not in movies:
        print(f"Movie '{title}' not found.")
        return

    movie_storage.delete_movie(title)

    print(f"Movie '{title}' deleted successfully.")


def update_movie():
    """
    Updates a movie rating.
    """
    movies = movie_storage.get_movies()

    title = get_valid_title()
    if title is None:
        return

    if title not in movies:
        print(f"Movie '{title}' not found.")
        return

    rating = get_valid_rating()
    if rating is None:
        return

    movie_storage.update_movie(title, rating)

    print(f"Movie '{title}' updated successfully.")


def movie_stats():
    """
    This function calculates the average rating, median rating, best movie,
    and the worst movie, and reports them.
    :param movies:
    :return:
    """

    movies = movie_storage.get_movies()
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
    """
    This function chooses a random movie from the list of movies and displays it.
    :param movies:
    :return:
    """
    movies = movie_storage.get_movies()
    movie = random.choice(list(movies.keys()))
    print(f"Your movie for tonight: {movie} ({movies[movie]["year"]}), it's rated {movies[movie]["rating"]}")


def search_movie():
    """
    This function searches for a movie based on the user's input.
    :param movies:
    :return:
    """

    movies = movie_storage.get_movies()
    query = input("Enter part of movie name: ")
    for movie in movies:
        if query.lower() in movie.lower():
            print(f"{movie} ({movies[movie]["year"]}), {movies[movie]["rating"]}")


def movies_sorted_by_rating():
    """
    This function sorts the movies by rating in descending order and displays them.
    :param movies:
    :return:
    """

    movies = movie_storage.get_movies()
    movies_sorted = sorted(movies.items(), key= lambda item: item[1]["rating"], reverse=True)
    for title, info in movies_sorted:
        print(f"{title}: {info['rating']}")





def main_menu():
    """
    Main menu of the application.
    """
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