import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

tmdb_key = os.getenv("TMDB_API_KEY")


def get_movie(movie):
    url = f"https://api.themoviedb.org/3/movie/{movie['movie']['ids']['tmdb']}?api_key={tmdb_key}&language=en-US"

    headers = {
        "accept": "application/json",
    }

    response = requests.get(url, headers=headers)

    details = response.json()
    movie["poster_path"] = f"https://image.tmdb.org/t/p/w185{details['poster_path']}"


def main():
    trakt_url = "https://api.trakt.tv/users/cfoster5/watched/movies"
    headers = {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": os.getenv("TRAKT_API_KEY"),
    }

    response = requests.get(trakt_url, headers=headers)
    watched_movies = response.json()
    for movie in watched_movies:
        get_movie(movie)

    # Sort the data by 'last_watched_at'
    sorted_data = sorted(watched_movies, key=lambda x: x["last_watched_at"])
    # Flatten properties such as "movie"
    df = pd.json_normalize(sorted_data)
    df.to_csv("data.csv", index=False)


if __name__ == "__main__":
    main()
