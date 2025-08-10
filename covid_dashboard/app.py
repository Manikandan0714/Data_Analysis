import streamlit as st
import pandas as pd
import datetime

# ---------------------
# Load Local CSV (Offline Mode)
# ---------------------
@st.cache_data
def load_data():
    df = pd.read_csv("owid-covid-data.csv", parse_dates=['date'])
    return df

st.title("🦠 COVID-19 Data Analytics Dashboard")
st.caption("Data Source: Our World in Data (Local File)")

df = load_data()

# ---------------------
# Sidebar Filters
# ---------------------
countries = sorted(df['location'].unique())
selected_country = st.sidebar.selectbox(
    "Select Country", 
    countries, 
    index=countries.index("India") if "India" in countries else 0
)

country_df = df[df['location'] == selected_country].sort_values("date")
latest = country_df.iloc[-1] if not country_df.empty else None

# ---------------------
# Safe Fetch Helper
# ---------------------
def safe_get(row, col):
    return row[col] if col in row.index and pd.notna(row[col]) else 0

# ---------------------
# Metrics Section
# ---------------------
st.subheader(f"📊 Latest COVID-19 Stats for {selected_country}")

if latest is not None:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cases", f"{int(safe_get(latest,'total_cases')):,}")
    col2.metric("Total Deaths", f"{int(safe_get(latest,'total_deaths')):,}")
    col3.metric("Cases per Million", f"{safe_get(latest,'total_cases_per_million'):,.2f}")
    col4.metric("Deaths per Million", f"{safe_get(latest,'total_deaths_per_million'):,.2f}")
else:
    st.warning("No data available for this country.")

# ---------------------
# Trend Chart
# ---------------------
st.subheader(f"📈 Trend of COVID-19 Cases in {selected_country}")
chart_data = country_df[['date', 'new_cases', 'new_deaths']].fillna(0)
chart_data = chart_data.set_index('date')
st.line_chart(chart_data)

# ---------------------
# Table View
# ---------------------
st.subheader("📅 Detailed Data Table")
st.dataframe(
    country_df[['date', 'total_cases', 'total_deaths', 'total_cases_per_million', 'total_deaths_per_million']].tail(20)
)

# ---------------------
# Date Filter & Insights
# ---------------------
st.sidebar.markdown("### Filter by Date")
start_date = st.sidebar.date_input("Start Date", country_df['date'].min().date() if not country_df.empty else datetime.date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", country_df['date'].max().date() if not country_df.empty else datetime.date.today())

mask = (country_df['date'] >= pd.to_datetime(start_date)) & (country_df['date'] <= pd.to_datetime(end_date))
filtered_df = country_df.loc[mask]

if not filtered_df.empty:
    st.sidebar.markdown(f"**Total cases in this period:** {int(filtered_df['new_cases'].sum()):,}")
    st.sidebar.markdown(f"**Total deaths in this period:** {int(filtered_df['new_deaths'].sum()):,}")
else:
    st.sidebar.warning("No data in selected date range.")
