import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="My Streamlit Dashboard",
    layout="wide"
)

# LOAD
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    return df

df = load_data()
st.write("Data loaded successfully!")
st.dataframe(df.head())

st.title(" Welcome to My Streamlit Dashboard")
st.markdown("Explore tracks by genre, popularity, and key musical features")


st.sidebar.header("Filters")

popularity_range = st.sidebar.slider(
    "Select Popularity Range",
    min_value=int(df["popularity"].min()),
    max_value=int(df["popularity"].max()),
    value=(0, 100)  #arbitrary range
)

show_explicit = st.sidebar.checkbox("Include Explicit Tracks", value=True)

genre = st.sidebar.selectbox("Select Genre", sorted(df["track_genre"].unique()))

filtered = df[
    (df["track_genre"] == genre) &
    (df["popularity"] >= popularity_range[0]) &
    (df["popularity"] <= popularity_range[1])
]

if not show_explicit:
    filtered = filtered[filtered["explicit"] == False]

st.subheader("Popularity vs Energy")
fig, ax = plt.subplots()
scatter = ax.scatter(
    filtered["energy"],
    filtered["popularity"],
    c=filtered["danceability"],
    cmap="viridis",
    alpha=0.8
)
ax.set_xlabel("Energy")
ax.set_ylabel("Popularity")
ax.set_title(f"Popularity vs Energy for {genre} Tracks")
fig.colorbar(scatter, ax=ax, label="Danceability")
st.pyplot(fig)

#Summary
st.write(f"Showing {len(filtered)} tracks in {genre} genre with popularity between "
         f"{popularity_range[0]}–{popularity_range[1]} "
         f"{'(explicit included)' if show_explicit else '(explicit excluded)'}")

st.subheader("Top 10 Artists by Average Popularity")
artist_avg = (
    filtered.groupby("artists")["popularity"].mean()
    .sort_values(ascending=False)
    .head(10)
)
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(artist_avg.index, artist_avg.values, color="skyblue", edgecolor="black")
ax.set_xlabel("Average Popularity")
ax.set_ylabel("Artist")
ax.invert_yaxis()
st.pyplot(fig)

st.subheader("Song Duration Distribution (ms)")
fig, ax = plt.subplots()
ax.hist(filtered["duration_ms"], bins=20, color="salmon", edgecolor="black")
ax.set_xlabel("Duration (ms)")
ax.set_ylabel("Count")
st.pyplot(fig)