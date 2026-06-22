import streamlit as st
import pandas as pd

# ==================================
# CONFIG
# ==================================
st.set_page_config(
    page_title="FIFA World Cup 2026",
    page_icon="⚽",
    layout="wide"
)

# ==================================
# LOAD DATA
# ==================================
@st.cache_data
def load_data():
    return pd.read_csv(
        "fifa_world_cup_2026_player_performance.csv",
        low_memory=False
    )

df = load_data()

# ==================================
# TITLE
# ==================================
st.title("⚽ FIFA World Cup 2026 Dashboard")

# ==================================
# FILTER
# ==================================
teams = sorted(df["team"].unique())

selected_team = st.selectbox(
    "Pilih Tim",
    ["Semua"] + teams
)

if selected_team != "Semua":
    df = df[df["team"] == selected_team]

# ==================================
# KPI
# ==================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Jumlah Pemain",
        df["player_name"].nunique()
    )

with col2:
    st.metric(
        "Total Goal",
        int(df["goals"].sum())
    )

with col3:
    st.metric(
        "Total Assist",
        int(df["assists"].sum())
    )

with col4:
    st.metric(
        "Rata-rata Rating",
        round(df["player_rating"].mean(), 2)
    )

# ==================================
# TOP SCORER
# ==================================
st.subheader("🏆 Top Scorer")

top_scorer = (
    df.groupby("player_name")["goals"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_scorer)

# ==================================
# TEAM GOALS
# ==================================
st.subheader("🌍 Goal per Tim")

team_goals = (
    df.groupby("team")["goals"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(team_goals)

# ==================================
# DATA TABLE
# ==================================
st.subheader("📋 Data Pemain")

st.dataframe(
    df,
    use_container_width=True
)
