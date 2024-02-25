import streamlit as st
import numpy as np
import pandas as pd
import pickle

with open('similarity.pkl','rb' ) as f:
    similarity = pickle.load(f)


books = pd.read_json('books.json')
# Use a wider layout
st.set_page_config(layout="wide")

# Read the DataFrame
popular_df = pd.read_json('popular.json')
pt = pd.read_json('pt.json')

# Set title as markdown

def recommend(book_name):
    index = np.where(pt.index== book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:6]
    data =[]
    for i in similar_items:
        items = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')
        items.extend(list(temp_df['Book-Title'].values))
        items.extend(list(temp_df['Book-Author'].values))
        items.extend(list(temp_df['Image-URL-M'].values))

        data.append(items)
    return data


def page1():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');

        .title {
            font-family: 'Lobster', cursive;
            font-size: 48px;
            font-weight: normal;
            color: #FFFFFF; /* Set color to white */
            text-align: center;
            margin-top: -50px;
        }
    </style>
    <h1 class="title">Top 50 Books</h1>
    """, unsafe_allow_html=True)

    st.write('\n')
    st.write('\n')

    # Display book information in columns
    cols = st.columns(5)
    for i in range(0, len(popular_df), 5):
        for j, col in enumerate(cols):
            index = i + j
            if index < len(popular_df):
                with col:
                    st.image(popular_df.loc[index, 'Image-URL-M'], width=150)
                    st.write(f"**Title:** {popular_df.loc[index, 'Book-Title']}")
                    st.write(f"**Author:** {popular_df.loc[index, 'Book-Author']}")
                    st.write(f"**Number of Ratings:** {popular_df.loc[index, 'num_rating']}")
                    st.write(f"**Average Rating:** {popular_df.loc[index, 'avg_rating']}")


def page2():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');

        .title {
            font-family: 'Lobster', cursive;
            font-size: 48px;
            font-weight: normal;
            color: white; /* Set the color to white  */
            text-align: center;
            margin-top: -50px;
        }

        .text {
            color: #FFFFFF; /* Set the color to white (#FFFFFF) */
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
    <h1 class="title">Collaborative Filtering Based Recommender Systems</h1>
    """, unsafe_allow_html=True)

    # Get user input for book name
    book_name = st.selectbox('Enter the Book Name to get recommendations', pt.index)

    if book_name:
        # Call the recommend function
        recommendations = recommend(book_name)

        # Display recommendations
        if recommendations:
            st.write('Top 5 recommendations:')
            num_cols = 3  # Number of columns to display recommendations
            num_recommendations = len(recommendations)
            num_rows = (num_recommendations + num_cols - 1) // num_cols

            for i in range(num_rows):
                cols = st.columns(num_cols)
                for j in range(num_cols):
                    index = i * num_cols + j
                    if index < num_recommendations:
                        with cols[j]:
                            st.image(recommendations[index][2], width=150)
                            st.write(f"**Title:** {recommendations[index][0]}")
                            st.write(f"**Author:** {recommendations[index][1]}")
                            st.write('---')  # Add a separator between recommendations
        else:
            st.write('No recommendations found.')

def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Go to', ['Popularity Based Recommendation', 'Collaborative Filtering Recommender Systems'])

    if page == 'Popularity Based Recommendation':
        page1()
    elif page == 'Collaborative Filtering Recommender Systems':
        page2()

if __name__ == "__main__":
    main()
