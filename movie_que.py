from dotenv import load_dotenv
import streamlit as st
import openai, os
import requests
import numpy as np

# Load environment variables
load_dotenv()

# Initialize openai client
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit app layout
def main():
    st.set_page_config(
        page_title="MovieQue",
        page_icon="🎬",
        layout="centered"
    )
    st.title("🍿 What to Watch Today?")

    # List of movie genres
    movie_genres = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Drama",
    "Fantasy", "Horror", "Mystery", "Romance", "Science Fiction", "Thriller",
    "War", "Western", "Biography", "Documentary", "Family", "Musical",
    "Sports", "Historical", "Superhero", "Psychological"
    ]
    rating_system_list = ["G", "PG", "PG-13", "R", "NC-17"]
    # User input for personal details
    with st.sidebar:
        st.subheader("🎭 Choose Your Preferences:")
        genres = st.multiselect('Genres', movie_genres)
        num_movies = st.slider('Number of Movies', min_value=1, max_value=10)
        languages = st.text_input('Languages')
        rating_system = st.selectbox('Rating System', rating_system_list)

    # Submit button
    if st.button("🚀 Get Recommendations"):
        recommended_show = movie_recommendation(genres, num_movies, languages, rating_system)
        st.subheader("🌟 Recommended Movies:")
        st.write(recommended_show)

# GPT function for generating dietary plan
def movie_recommendation(genres, num_movies, languages, rating_system):
    assistant_content = """
    1. The Princess Bride (1987)

    * Synopsis: This cult classic is a hilarious and heartwarming adventure about a farmhand named Westley who must rescue his true love Princess Buttercup from the evil Prince Humperdinck.  Westley faces many challenges and transformations along the way,  with a little  bit of magic  included. This movie is perfect for the whole family.

    2. The Lost City (2022)
    * Synopsis: Sandra Bullock stars as a reclusive romance novelist who is kidnapped by a crazy billionaire who believes her latest book holds the key to finding an ancient treasure. Channing Tatum plays the cover model for her book who is thrown into the jungle to rescue her.  This is a fun and action-packed adventure with a great romance at its center.
    
    3. Stardust (2007)
    * Synopsis: In a small English village, a young man named Tristan ventures into a magical world  to retrieve a fallen star for his beloved.  There he encounters danger,  flying pirates,  a wicked witch, and a beautiful woman who is not what she seems. This movie is a visually stunning and charming adventure with a touch of fantasy.
    """

    user_input = f"""
    I want to watch movie with genre of {', '.join(genres)}. I want {num_movies} movies. I want the {languages} for all these movies. I want the {rating_system} for the rating system of these movies.
    """
    message = [
            {
                'role': 'system', 
                'content':f"You are a movie expertise that assist people in recommending movie or series. Recommend movie based on user input. You also include a little bit of synopsis for that show"
            },
            {   'role': 'user',
                'content':"I want to watch movie with genre of romance, adventure. I want 3 movies. I want the English languages for all these movies. I want the PG-13 for the rating system of these movies."
            },
            {   'role': 'assistant',
                'content': assistant_content
            },
            {   'role': 'user',
                'content':user_input
            }
        ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=message,
        max_tokens=1000
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    main()
