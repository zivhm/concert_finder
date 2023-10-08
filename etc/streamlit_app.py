import streamlit as st
import pandas as pd
import numpy as np
import json

import plotly.express as px


@st.cache_data  # Use st.cache_data instead of st.cache
def load_data():
    df1 = pd.read_json(r'C:\Users\Ziv\Downloads\my_spotify_data\MyData\StreamingHistory0.json')
    df2 = pd.read_json(r'C:\Users\Ziv\Downloads\my_spotify_data\MyData\StreamingHistory1.json')
    df = pd.concat([df1, df2], axis=0, ignore_index=True)

    df['minsPlayed'] = df['msPlayed'] / (1000 * 60)
    df["endTime"] = pd.to_datetime(df["endTime"]).dt.date
    return df


def summarize_df(df):
    st.header('Your Spotify Consumption Summary:')

    total_mins = df['minsPlayed'].sum()
    total_mins_hr = total_mins / 60
    total_mins_days = total_mins_hr / 24

    st.subheader(
        f"You've spent roughly {np.round(total_mins_hr, 2)} hours listening to Spotify. That's about {np.round(total_mins_days, 2)} total days!")

    top_artist_name = df_sorted_artists['artistName'].values[0]
    top_artist_time_mins = df_sorted_artists_min['minsPlayed'].values[0]
    top_artist_time_hrs = top_artist_time_mins / 60
    st.subheader(f"Your top artist is {top_artist_name}, with approximately {np.round(top_artist_time_hrs, 2)} hours of play time.")

    top_track_name = df_sorted_tracks['trackName'].values[0]
    top_track_time_mins = df_sorted_tracks_min['minsPlayed'].values[0]
    top_track_time_hrs = top_track_time_mins / 60

    st.subheader(f"Your top track is {top_track_name}', with approximately {np.round(top_track_time_hrs, 2)} hours of play time.")

    unique_artists = df['artistName'].nunique()
    unique_tracks = df['trackName'].nunique()

    st.subheader(f"You've listened to songs from {unique_artists} different artists and {unique_tracks} unique tracks in total!")

    earliest_date = df["endTime"].min()
    latest_date = df["endTime"].max()

    st.subheader(f"Your listening history ranges from {earliest_date} to {latest_date}")



df = load_data()

# Group data
df_grouped_tracks = df.groupby(["trackName", "artistName"]).size().reset_index(name="timesPlayed")
df_grouped_artists = df.groupby("artistName").size().reset_index(name="timesPlayed")
df_grouped_day = df.groupby("endTime").agg({"minsPlayed": "sum"}).reset_index()

# Sorting and get top 100 tracks and artists
df_sorted_tracks = df_grouped_tracks.sort_values("timesPlayed", ascending=False).head(100)
df_sorted_artists = df_grouped_artists.sort_values("timesPlayed", ascending=False).head(100)

# Adds grouped data for total minutes played by artist
df_grouped_artists_min = df.groupby("artistName").agg({"minsPlayed": "sum"}).reset_index()

# Sorting and get top 100 artists by total minutes played
df_sorted_artists_min = df_grouped_artists_min.sort_values("minsPlayed", ascending=False).head(100)

# Group data - total minutes played by track
df_grouped_tracks_min = df.groupby(["trackName", "artistName"]).agg({"minsPlayed": "sum"}).reset_index()

# Sorting and get top 100 tracks by total minutes played
df_sorted_tracks_min = df_grouped_tracks_min.sort_values("minsPlayed", ascending=False).head(100)


st.title("Spotify Streaming History")

st.header("Listening behavior over time")
fig = px.line(df_grouped_day, x='endTime', y='minsPlayed')
fig.update_layout(
    height=450,      # You can adjust the height as needed
    width=1000,      # You can adjust the width as needed
)

st.plotly_chart(fig)

st.header("Top 100 Tracks by number of times played")
fig = px.bar(df_sorted_tracks, x='trackName', y='timesPlayed', color='timesPlayed', title="Top 100 Tracks by Number of Plays")
fig.update_layout(
    height=450,      # You can adjust the height as needed
    width=1000,      # You can adjust the width as needed
)
st.plotly_chart(fig)

st.header("Top 100 Artists by number of times played")
fig = px.bar(df_sorted_artists, x='artistName', y='timesPlayed', color='timesPlayed', title="Top 100 Artists by Number of Plays")
fig.update_layout(
    height=450,  # You can adjust the height as needed
    width=1000,  # You can adjust the width as needed
)
st.plotly_chart(fig)

st.header("Top 100 Artists by Total Minutes Played")
fig = px.bar(df_sorted_artists_min, x='artistName', y='minsPlayed', color='minsPlayed', title="Top 100 Artists by Total Minutes Played")
fig.update_layout(height=450, width=1000)
st.plotly_chart(fig)

st.header("Top 100 Tracks by Total Minutes Played")
fig = px.bar(df_sorted_tracks_min, x='trackName', y='minsPlayed', color='minsPlayed', title="Top 100 Tracks by Total Minutes Played")
fig.update_layout(height=450, width=1000)

st.plotly_chart(fig)

summarize_df(df)
