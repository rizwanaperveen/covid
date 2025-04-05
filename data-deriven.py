import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="COVID-19 Tracker", layout="wide")

st.title("🌍 COVID-19 Tracker Dashboard")

# Fetch list of countries
@st.cache_data
def get_countries():
    url = "https://disease.sh/v3/covid-19/countries"
    response = requests.get(url)
    data = response.json()
    return sorted([country["country"] for country in data])

# Fetch COVID stats for a country
def get_country_data(country):
    url = f"https://disease.sh/v3/covid-19/countries/{country}?strict=true"
    response = requests.get(url)
    return response.json()

# Fetch historical data
def get_historical_data(country):
    url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays=30"
    response = requests.get(url)
    data = response.json()
    return data.get("timeline", {}) if "timeline" in data else {}

# Country selection
countries = get_countries()
selected_country = st.selectbox("Choose a Country", countries, index=countries.index("India"))

# Get current stats
data = get_country_data(selected_country)

# Display metrics
st.subheader(f"📊 Current Stats for {selected_country}")
col1, col2, col3 = st.columns(3)
col1.metric("✅ Total Cases", f"{data['cases']:,}")
col2.metric("💚 Recovered", f"{data['recovered']:,}")
col3.metric("❌ Deaths", f"{data['deaths']:,}")

# Get and plot historical data
history = get_historical_data(selected_country)

if history:
    df = pd.DataFrame(history["cases"], index=[0]).T
    df.columns = ["cases"]
    df["daily_cases"] = df["cases"].diff().fillna(0)
    df.index = pd.to_datetime(df.index)

    st.subheader("📈 Daily New Cases (Last 30 Days)")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df.index, df["daily_cases"], marker="o", linestyle="-", color="orange")
    ax.set_ylabel("Daily Cases")
    ax.set_xlabel("Date")
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("⚠️ Historical data not available for this country.")

st.caption("Data sourced from disease.sh API")
