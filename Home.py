import streamlit as st
import pickle
import pandas as pd
import requests
import random
import time
from streamlit_extras.switch_page_button import switch_page
import base64

st.set_page_config(
    page_title='MoviesGPT',
    page_icon = '📽️'
)

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

st.title('MoviesGPT')
st.subheader('(Movie Recommendation System)')

# Define a function to generate a random number based on user input
def generate_number(user_input):
    # Use the current time to seed the random number generator
    random.seed(int(time.time()))
    # Generate a random number between 0 and 100
    random_number = random.randint(0, 100)
    return random_number

# Define the Streamlit app
# Set the title and page layout
    # Add a title and description to the app
    # Add a text input box for the user to enter inpu
# movies_list = pickle.load(open('movies.pkl','rb'))
# movies_list = movies_list['title'].values


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


st.subheader("Enter your basic details:")
name = st.text_input("Name:")
age = st.number_input("Age:", value=0, step=1)
gender = st.selectbox("Gender:", options=["Male", "Female", "Other"])


if 'random_seed' not in st.session_state:
    st.session_state['random_seed'] = 0

# Add a button to trigger the number generation
if st.button("Submit"):
    # Call the generate_number function with the user input as an argument
    st.session_state.random_seed = int(age)
    switch_page('Movies')


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


