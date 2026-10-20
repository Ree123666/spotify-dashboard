# Spotify Curation Dashboard —  <Lu Jialing>

## Step 1 — Dataset and Decision-Maker

**Dataset:** Kaggle Spotify Songs (`songs_normalize.csv`).
Link: <Kaggle >
About 2,000 tracks, one row per song, covering 1998–2019. Columns include artist,
song, duration, explicit flag, year, popularity (0–100), Spotify audio features
(danceability, energy, valence, tempo, acousticness, instrumentalness,
speechiness, liveness, loudness, key, mode) and genre (multi-label, some missing).
Real data scraped from Spotify, not synthetic. Some years and genres have gaps.

**Decision-maker:** Content Curation Lead at a music streaming platform.

## Step 2 — Why a Dashboard

- Who looks at it, how often: the Content Curation Lead, once a week when
  planning playlists and homepage placement.
- Decision supported: "If the Content Curation Lead sees that high-popularity
  tracks in a given era/genre cluster around certain audio features (e.g. high
  danceability + high valence), they will prioritize tracks matching those
  features in next week's high-exposure slots."
- What they do today / cost: manually scan spreadsheets and pick by intuition,
  costing hours per week and risking missed high-potential tracks.
- Why a dashboard, not an email/report/alert: the same questions recur weekly
  for the same person and drive action.

## Step 3 — What We Show and What We Cut

**Headline metrics:**
1. Tracks in current selection
2. Average popularity
3. High-popularity share (popularity ≥ 70)

**Supporting charts:**
- Average popularity by year
- Danceability vs valence by genre

**Filters:** Year range slider; genre multi-select; explicit-only toggle.

**Two things we chose NOT to show, and why:**
1. Loudness / key / mode distributions — interesting in EDA but the curation
   lead would not change playlist decisions based on musical key.
2. Detailed duration distribution — not a key weekly decision variable; it
   would dilute the important charts.

**Data pitfalls and how the dashboard handles them:**
- Genre is multi-label with missing values (`set()`): we take the first (main)
  genre and map missing to "Unknown"; noted in a caption.
- Popularity is a Spotify snapshot, not live: stated in a caption.
- Year may reflect re-release year for some tracks: stated in a caption.

**Order:** headline metrics → explanatory charts → optional underlying rows.

## Step 4 — Refresh Frequency

- Production refresh: weekly (Monday early morning) from Spotify API / data
  warehouse. Rationale: playlist curation is a weekly decision; real-time
  refresh adds cost without changing decisions.
- Review frequency: weekly, Monday morning — same as refresh.
- Tracked metric and trigger: high-popularity share (≥70). If a genre's share
  drops more than 10 percentage points week-over-week, a manual review is
  triggered.
- Cost of stale data: a one-week lag could miss a rising genre window and waste
  exposure; a one-day lag has limited impact.

**Line shown on the dashboard:**
`Data: 1998–2019, Kaggle Spotify snapshot | Production refresh: weekly (Monday)`

## Step 5 — Build and Deploy

Built with `uv init`, deployed on Streamlit Cloud (Python 3.14).
App URL: <[app URL](https://final-data-analysis-app-ap3ye7xhqhkgada9kqg476.streamlit.app/)>
Repo URL: <[GitHub 仓库 URL](https://github.com/Ree123666/spotify-dashboard)>
