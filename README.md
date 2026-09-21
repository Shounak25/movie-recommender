# Movie Recommender System

A content-based movie recommender built with Streamlit. Pick a movie and get
5 similar recommendations with posters.

## Features
- Recommendations based on cosine similarity
- Posters fetched from the TMDB API (parallel, with retries)
  

## Tech
Python, Streamlit, pandas, TMDB API

## Run locally
1. `pip install -r requirements.txt`
2. Create `.streamlit/secrets.toml` with `TMDB_API_KEY = "your_key"`
3. `streamlit run app.py`
