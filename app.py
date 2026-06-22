import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="FIFA World Cup 2026 Dashboard",
    page_icon="⚽",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("fifa_world_cup_2026_player_performance.csv")
    df["match_date"] = pd.to_datetime(df["match_date"])
    return df

df = load_data()

# =========================
# TITLE
# =========================
st.title("⚽ FIFA World Cup 2026 Player Performance Dashboard")
st.markdown("Analisis performa pemain selama turnamen.")

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("Filter")

teams = sorted(df["team"].dropna().unique())
positions = sorted(df["position"].dropna().unique())

selected_team = st.sidebar.multiselect(
    "Pilih Tim",
    teams,
    default=teams[:5]
)

selected_position = st.sidebar.multiselect(
    "Pilih Posisi",
    positions,
    default=positions
)

filtered_df = df[
    (df["team"].isin(selected_team)) &
    (df["position"].isin(selected_position))
]

# =========================
# KPI
# =========================
st.subheader("📊 Ringkasan")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Jumlah Pemain",
    filtered_df["player_name"].nunique()
)

col2.metric(
    "Total Goal",
    int(filtered_df["goals"].sum())
)

col3.metric(
    "Total Assist",
    int(filtered_df["assists"].sum())
)

col4.metric(
    "Rata-rata Rating",
    round(filtered_df["player_rating"].mean(), 2)
)

# =========================
# TOP PLAYER
# =========================
st.subheader("🏆 Top 10 Player berdasarkan Tournament Rating")

top_players = (
    filtered_df.groupby(["player_name", "team"], as_index=False)
    .agg({
        "tournament_rating": "mean",
        "goals": "sum",
        "assists": "sum"
    })
    .sort_values("tournament_rating", ascending=False)
    .head(10)
)

fig_top = px.bar(
    top_players,
    x="player_name",
    y="tournament_rating",
    color="team",
    title="Top 10 Tournament Rating"
)

st.plotly_chart(fig_top, use_container_width=True)

# =========================
# GOAL VS ASSIST
# =========================
st.subheader("⚽ Goal vs Assist")

player_stats = (
    filtered_df.groupby(["player_name", "team"], as_index=False)
    .agg({
        "goals": "sum",
        "assists": "sum",
        "player_rating": "mean"
    })
)

fig_scatter = px.scatter(
    player_stats,
    x="goals",
    y="assists",
    size="player_rating",
    color="team",
    hover_name="player_name",
    title="Perbandingan Goal dan Assist"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# =========================
# TEAM PERFORMANCE
# =========================
st.subheader("🌍 Performa Tim")

team_stats = (
    filtered_df.groupby("team", as_index=False)
    .agg({
        "goals": "sum",
        "assists": "sum",
        "player_rating": "mean"
    })
    .sort_values("goals", ascending=False)
)

fig_team = px.bar(
    team_stats,
    x="team",
    y="goals",
    color="player_rating",
    title="Total Goal per Tim"
)

st.plotly_chart(fig_team, use_container_width=True)

# =========================
# POSITION ANALYSIS
# =========================
st.subheader("📌 Analisis Posisi")

position_stats = (
    filtered_df.groupby("position", as_index=False)
    .agg({
        "goals": "sum",
        "assists": "sum",
        "player_rating": "mean"
    })
)

fig_position = px.bar(
    position_stats,
    x="position",
    y="player_rating",
    color="position",
    title="Rata-rata Rating per Posisi"
)

st.plotly_chart(fig_position, use_container_width=True)

# =========================
# PLAYER DETAIL
# =========================
st.subheader("🔍 Detail Pemain")

players = sorted(filtered_df["player_name"].unique())

selected_player = st.selectbox(
    "Pilih Pemain",
    players
)

player_df = filtered_df[
    filtered_df["player_name"] == selected_player
]

col1, col2 = st.columns(2)

with col1:
    st.metric("Goal", int(player_df["goals"].sum()))
    st.metric("Assist", int(player_df["assists"].sum()))
    st.metric("Rating", round(player_df["player_rating"].mean(), 2))

with col2:
    st.metric(
        "Minutes Played",
        int(player_df["minutes_played"].sum())
    )
    st.metric(
        "Tournament Rating",
        round(player_df["tournament_rating"].mean(), 2)
    )

st.dataframe(player_df)

# =========================
# DOWNLOAD
# =========================
st.subheader("⬇️ Download Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_player_performance.csv",
    mime="text/csv"
)
