import streamlit as st
import pandas as pd

st.set_page_config(page_title="Spotify Curation Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("songs_normalize.csv")

df = load_data()

def main_genre(g):
    if pd.isna(g):
        return "Unknown"
    s = str(g).strip()
    if s in ("", "set()", "set([])", "{}"):
        return "Unknown"
    return s.split(",")[0].strip()

df["main_genre"] = df["genre"].apply(main_genre)
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")
df = df.dropna(subset=["year", "popularity"]).copy()
df["year"] = df["year"].astype(int)

st.title("Spotify Curation Dashboard — Team Data Crew")
st.caption("For the Content Curation Lead. Decision: which genres/eras to prioritize in weekly playlist and homepage placement.")

year_min, year_max = int(df["year"].min()), int(df["year"].max())
year_range = st.slider("Year range", year_min, year_max, (year_min, year_max))

genres = sorted(df["main_genre"].unique())
sel_genres = st.multiselect("Genres", genres, default=genres)

explicit_only = st.checkbox("Explicit only", value=False)

mask = df["year"].between(year_range[0], year_range[1]) & df["main_genre"].isin(sel_genres)
if explicit_only:
    mask &= df["explicit"].astype(str).str.lower() == "true"
d = df[mask]

c1, c2, c3 = st.columns(3)
c1.metric("Tracks", f"{len(d):,}")
c2.metric("Avg popularity", f"{d['popularity'].mean():.1f}" if len(d) else "—")
high_share = (d["popularity"] >= 70).mean() * 100 if len(d) else 0
c3.metric("High-popularity share (≥70)", f"{high_share:.1f}%")

if len(d) == 0:
    st.warning("No tracks match the current filters.")
    st.stop()

# 图1：用 Streamlit 内置折线图，不需要 matplotlib
st.subheader("Average popularity by year")
era = d.groupby("year")["popularity"].mean().reset_index()
st.line_chart(era, x="year", y="popularity")

# 图2：用 Streamlit 内置散点图，不需要 matplotlib
st.subheader("Danceability vs valence by genre")
g = d.groupby("main_genre")[["danceability", "valence"]].mean().dropna().reset_index()
st.scatter_chart(g, x="danceability", y="valence", color="main_genre")

st.caption("Data: 1998–2019, Kaggle Spotify snapshot | Production refresh: weekly (Monday)")

with st.expander("Underlying rows (top 200)"):
    cols = ["artist", "song", "year", "popularity", "main_genre", "danceability", "valence"]
    st.dataframe(d[cols].sort_values("popularity", ascending=False).head(200))
