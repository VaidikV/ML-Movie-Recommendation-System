import streamlit as st
import pickle
import requests

movies_list = pickle.load(open('movies_pkl', 'rb'))
movies_title = movies_list['title'].values
similarity = pickle.load(open('similarity', 'rb'))


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=483c8ddeb7e13b2229ec717cffd72739'.format(movie_id))
    try:
        picture = response.json()['poster_path']
        link = "https://image.tmdb.org/t/p/w500/" + picture
    except:
        link = "Poster Not Found"
    return link


def recommend(movie):
    recommended_movies = []
    recommended_movies_posters = []
    try:
        movie_index = movies_list[movies_list['title'] == movie].index[0]
    except IndexError:
        print("Movie Not Found...")
    else:
        distances = similarity[movie_index]
        final_movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

        for i in final_movies_list:
            movie_id = movies_list.iloc[i[0]].id
            recommended_movies.append(movies_list.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters


st.title("Movie Recommendation System")
movie_name = st.selectbox('Search for a movie that you like!', movies_title)

if st.button('Recommend'):
    names, posters = recommend(movie_name)

    # for i in recommend(movie_name):
    #     st.write(i)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        try:
            st.image(posters[0])
        except:
            st.write("Poster not found.")

    with col2:
        st.text(names[1])
        try:
            st.image(posters[1])
        except:
            st.write("Poster not found.")

    with col3:
        st.text(names[2])
        try:
            st.image(posters[2])
        except:
            st.write("Poster not found.")

    with col4:
        st.text(names[3])
        try:
            st.image(posters[3])
        except:
            st.write("Poster not found.")

    with col5:
        st.text(names[4])
        try:
            st.image(posters[4])
        except:
            st.write("Poster not found.")