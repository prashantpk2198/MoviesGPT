import streamlit as st
import base64

st.title('Recommendations For You')
col1, col2, col3, col4, col5 = st.columns(5)
a = [col1, col2, col3, col4, col5]

for i in range(5):
    with a[i]:
        st.text(st.session_state.names[i])
        st.image(st.session_state.posters[i])

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