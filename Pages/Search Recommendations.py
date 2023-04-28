import streamlit as st
import pickle
import pandas as pd
import requests
import random
import time
import base64

st.set_page_config(
    page_title='MoviesGPT',
    page_icon = '📽️'
)

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


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=e1e21c048f73bffe07d41266b325e08a&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w780/" + data['poster_path']

def recommend_movies(movie_list):
    recommended_movies = []
    recommended_movies_poster = []
    total = movie_list
    for i in range(3):
        movie_index = movies[movies['title'] == movie_list[i]].index[0]
        movies_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:10]
        movie_name = []
        counter=0
        for j in movies_list:
            movie_name = movies.iloc[j[0]].title
            movie_id = movies.iloc[j[0]].movie_id
            if movie_name in total:
                continue
            else:
                counter+=1
                recommended_movies.append(movie_name)
                recommended_movies_poster.append(fetch_poster(movie_id))

                total+=[movie_name]
                if i==0:
                    if counter==3:
                        break
                if i>0:
                    if counter==1:
                        break
    return recommended_movies, recommended_movies_poster

st.title('Search Your Favourite Movie')

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox(
    'Movie you like to be recommended?',
    movies['title'].values
)
array = [selected_movie_name,selected_movie_name,selected_movie_name]

if st.button('Recommend'):
    names, posters = recommend_movies(array)

    col1, col2, col3, col4, col5 = st.columns(5)
    a = [col1, col2, col3, col4, col5]

    for i in range(5):
        with a[i]:
            st.text(names[i])
            st.image(posters[i])










