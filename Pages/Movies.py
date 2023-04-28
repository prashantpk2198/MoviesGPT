from Home import fetch_poster
from Home import movies, recommend_movies
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import base64
import random

st.title('Select Your Top3 Movies')


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('C:/Users/prash/PycharmProjects/movie-recommender-system/Bgpic.jpeg')


random_20 = movies.sample(n=20, random_state=st.session_state.random_seed)
# Select a random subset of 20 movies
# Display the movie names in a 5x4 grid
col1, col2, col3, col4, col5 = st.columns(5)
cols = [col1, col2, col3, col4, col5]
i = 0
for col in cols:
    for j in range(4):
        movie_id = random_20['movie_id'].values
        col.image(fetch_poster(movie_id[i]), use_column_width=True)
        i += 1

# taking preferences
# Create a dictionary to keep track of which movies have been selected
selected_movies = {"first": None, "second": None, "third": None}

arrays = []
for i in range(3):
    key = f"recommended_movie_{i}"

    # Create a selectbox for the movie choice
    movie_names = random_20['title'].values
    options = [movie for movie in movie_names if movie not in arrays]
    selected_movies[f"choice_{i + 1}"] = st.selectbox(f"{i + 1}. Choose a movie", options=options, key=key)
    arrays.append(selected_movies[f"choice_{i + 1}"])
a = list(selected_movies.values())
array = a[3:6]

if 'names' not in st.session_state:
    st.session_state['names'] = []

if 'posters' not in st.session_state:
    st.session_state['posters'] = []

if st.button('Recommend'):
    st.session_state.names, st.session_state.posters = recommend_movies(array)
    switch_page('Recommendations')
