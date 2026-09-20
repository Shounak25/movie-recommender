import streamlit as st
import pickle
import pandas as pd
import requests
import os



def get_api_key():
    try:
        return st.secrets["TMDB_API_KEY"]
    except Exception:
        return os.environ.get("TMDB_API_KEY", "")

TMDB_API_KEY = get_api_key()
# -------------------------------
# Fetch movie poster from TMDB
# -------------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

        return None

    except requests.exceptions.RequestException as e:
        print("TMDB error:", e)
        return None


# -------------------------------
# Load movie data
# -------------------------------
movies_dict = pickle.load(
    open("movies.pkl", "rb")
)

movies = pd.DataFrame(movies_dict)

similarity = pickle.load(
    open("similarity.pkl", "rb")
)

movies_list = movies["title"].values


# -------------------------------
# Streamlit UI
# -------------------------------
st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies_list
)


# -------------------------------
# Recommendation function
# -------------------------------
def recommend(movie):

    # Find index of selected movie
    movie_index = movies[
        movies["title"] == movie
    ].index[0]

    # Similarity scores for this movie
    distances = similarity[movie_index]

    # Get 5 most similar movies
    movie_indices = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in movie_indices:

        # Get TMDB movie ID
        movie_id = movies.iloc[i[0]].movie_id

        # Get movie title
        movie_name = movies.iloc[i[0]].title

        # Get poster
        poster = fetch_poster(movie_id)

        recommended_movie_names.append(movie_name)
        recommended_movie_posters.append(poster)

    return (
        recommended_movie_names,
        recommended_movie_posters
    )


# -------------------------------
# Recommend button
# -------------------------------
if st.button("Recommend"):

    recommended_movie_names, recommended_movie_posters = recommend(
        selected_movie_name
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])

        if recommended_movie_posters[0]:
            st.image(recommended_movie_posters[0])

    with col2:
        st.text(recommended_movie_names[1])

        if recommended_movie_posters[1]:
            st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])

        if recommended_movie_posters[2]:
            st.image(recommended_movie_posters[2])

    with col4:
        st.text(recommended_movie_names[3])

        if recommended_movie_posters[3]:
            st.image(recommended_movie_posters[3])

    with col5:
        st.text(recommended_movie_names[4])

        if recommended_movie_posters[4]:
            st.image(recommended_movie_posters[4])




