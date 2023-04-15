import pandas as pd
import streamlit as st

# Load the dataset
df = pd.read_csv('Data.csv')
# Convert 'created_at' column to datetime format
df['created_at'] = pd.to_datetime(df['created_at'])

# Convert 'replies' column to numeric format
df['replies'] = pd.to_numeric(df['replies'], errors='coerce')
# Create a function to filter the tweets based on user input
def filter_tweets(df, hashtag=None, likes=None, replies=None, location=None):
    if hashtag:
        df = df[df['hashtags'].str.contains(hashtag, case=False)]
    if likes:
        likes = int(likes)
        df = df[df['likes'] >= likes]
    if replies:
        replies = int(replies)
        df = df[pd.notnull(df['replies'])]
        df = df[df['replies'] >= replies]
    if location:
        df = df[df['user_location'].str.contains(location, case=False)]
    return df

# Define the Streamlit app
def app():
    # Add a title and subtitle
    st.title("Twitter Recommendation System")
    st.write("Enter your search criteria and we'll recommend some tweets!")

    # Add input fields for the user to enter their search criteria
    hashtag = st.text_input("Hashtag")
    likes = st.number_input("Minimum number of likes", min_value=0, step=1)
    replies = st.number_input("Minimum number of replies", min_value=0, step=1)
    location = st.text_input("Location")

    # Filter the tweets based on the user input
    filtered_tweets = filter_tweets(df, hashtag, likes, replies, location)

    # Display the recommended tweets along with their corresponding features
    if not filtered_tweets.empty:
        st.write(f"Recommended tweets ({len(filtered_tweets)} tweets found):")
        for index, row in filtered_tweets.iterrows():
            st.write(f"Tweet: {row['text']}")
            st.write(f"Hashtags: {row['hashtags']}")
            st.write(f"Likes: {row['likes']}")
            st.write(f"Replies: {row['replies']}")
            st.write(f"Location: {row['user_location']}")
            st.write("----")
    else:
        st.write("No tweets found with the selected criteria.")
app()
