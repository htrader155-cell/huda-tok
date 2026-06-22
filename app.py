import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="Global EV Adoption Dashboard",
    page_icon="🚗",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    return pd.read_csv(
        "global_ev_adoption_behavior_2026.csv",
        low_memory=False
    )

df = load_data()

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("🔍 Filter")

city_options = sorted(df["city_type"].unique())
education_options = sorted(df["education_level"].unique())

selected_city = st.sidebar.selectbox(
    "City Type",
    ["All"] + city_options
)

selected_education = st.sidebar.selectbox(
    "Education Level",
    ["All"] + education_options
)

filtered_df = df.copy()

if selected_city != "All":
    filtered_df = filtered_df[
        filtered_df["city_type"] == selected_city
    ]

if selected_education != "All":
    filtered_df = filtered_df[
        filtered_df["education_level"] == selected_education
    ]

# =====================================================
# TITLE
# =====================================================
st.title("🚗 Global EV Adoption Behavior 2026 Dashboard")

st.markdown(
    "Analisis faktor-faktor yang memengaruhi adopsi kendaraan listrik (EV)."
)

# =====================================================
# KPI
# =====================================================
total_people = len(filtered_df)

avg_income = filtered_df["annual_income"].mean()

avg_commute = filtered_df["daily_commute_km"].mean()

high_adoption_pct = (
    (filtered_df["ev_adoption_likelihood"] == "High").mean()
    * 100
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Jumlah Responden", f"{total_people:,}")
c2.metric("Rata-rata Income", f"${avg_income:,.0f}")
c3.metric("Daily Commute", f"{avg_commute:.1f} km")
c4.metric("High Adoption", f"{high_adoption_pct:.1f}%")

# =====================================================
# ADOPTION DISTRIBUTION
# =====================================================
st.subheader("📊 EV Adoption Likelihood")

adoption_count = (
    filtered_df["ev_adoption_likelihood"]
    .value_counts()
    .reset_index()
)

adoption_count.columns = [
    "Likelihood",
    "Count"
]

fig1 = px.pie(
    adoption_count,
    names="Likelihood",
    values="Count"
)

st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# AGE ANALYSIS
# =====================================================
st.subheader("👥 Usia vs EV Adoption")

fig2 = px.box(
    filtered_df,
    x="ev_adoption_likelihood",
    y="age"
)

st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# INCOME ANALYSIS
# =====================================================
st.subheader("💰 Pendapatan vs EV Adoption")

income_df = (
    filtered_df.groupby(
        "ev_adoption_likelihood",
        as_index=False
    )["annual_income"]
    .mean()
)

fig3 = px.bar(
    income_df,
    x="ev_adoption_likelihood",
    y="annual_income"
)

st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# ENVIRONMENTAL AWARENESS
# =====================================================
st.subheader("🌱 Environmental Awareness")

env_df = (
    filtered_df.groupby(
        "ev_adoption_likelihood",
        as_index=False
    )["environmental_awareness_score"]
    .mean()
)

fig4 = px.bar(
    env_df,
    x="ev_adoption_likelihood",
    y="environmental_awareness_score"
)

st.plotly_chart(fig4, use_container_width=True)

# =====================================================
# TECHNOLOGY AFFINITY
# =====================================================
st.subheader("📱 Technology Affinity")

tech_df = (
    filtered_df.groupby(
        "ev_adoption_likelihood",
        as_index=False
    )["technology_affinity_score"]
    .mean()
)

fig5 = px.bar(
    tech_df,
    x="ev_adoption_likelihood",
    y="technology_affinity_score"
)

st.plotly_chart(fig5, use_container_width=True)

# =====================================================
# CHARGING ACCESSIBILITY
# =====================================================
st.subheader("🔌 Charging Accessibility")

charge_df = (
    filtered_df.groupby(
        "ev_adoption_likelihood",
        as_index=False
    )["charging_station_accessibility"]
    .mean()
)

fig6 = px.bar(
    charge_df,
    x="ev_adoption_likelihood",
    y="charging_station_accessibility"
)

st.plotly_chart(fig6, use_container_width=True)

# =====================================================
# HOME CHARGING
# =====================================================
st.subheader("🏠 Home Charging Availability")

home_df = (
    filtered_df.groupby(
        "home_charging_available"
    )
    .size()
    .reset_index(name="count")
)

home_df["home_charging_available"] = (
    home_df["home_charging_available"]
    .replace({0: "No", 1: "Yes"})
)

fig7 = px.pie(
    home_df,
    names="home_charging_available",
    values="count"
)

st.plotly_chart(fig7, use_container_width=True)

# =====================================================
# CORRELATION
# =====================================================
st.subheader("📈 Faktor Numerik")

numeric_cols = [
    "annual_income",
    "daily_commute_km",
    "fuel_expense_per_month",
    "charging_station_accessibility",
    "environmental_awareness_score",
    "technology_affinity_score",
    "range_anxiety_score",
    "ev_knowledge_score"
]

st.dataframe(
    filtered_df[numeric_cols]
    .describe()
    .round(2),
    use_container_width=True
)

# =====================================================
# RAW DATA
# =====================================================
with st.expander("📄 Lihat Data"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# =====================================================
# DOWNLOAD
# =====================================================
csv = filtered_df.to_csv(index=False)

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    file_name="ev_adoption_filtered.csv",
    mime="text/csv"
)
