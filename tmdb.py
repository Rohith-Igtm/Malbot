import requests
import os

API_KEY = os.getenv("TMDB_API_KEY")


def search_movie(movie_name):

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": API_KEY,
        "query": movie_name
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        results = data.get("results", [])

        if not results:
            return None

        return results[0]

    except Exception as e:

        print("\n❌ TMDB REQUEST FAILED")
        print(e)

        return None

def verify_malayalam_movie(movie_name):

    result = search_movie(movie_name)

    if not result:
        return None

    if result.get("original_language") != "ml":
        return None

    return {

        "title": result.get("title"),

        "release_date": result.get("release_date"),

        "poster_path": result.get("poster_path"),

        "tmdb_id": result.get("id")

    }