import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="EV Market Dashboard", layout="wide")
st.title("Electric Vehicle Market Dashboard")
st.caption("A simple dashboard for reviewing EV sales, manufacturers, battery technologies, range, and customer ratings.")

@st.cache_data
def load_data():
    return pd.read_csv("data/ev_market_sample.csv")

df = load_data()

st.sidebar.header("Filters")
years = sorted(df["year"].unique())
selected_years = st.sidebar.multiselect("Year", years, default=years)
categories = sorted(df["vehicle_category"].unique())
selected_categories = st.sidebar.multiselect("Vehicle category", categories, default=categories)
manufacturers = sorted(df["manufacturer"].unique())
selected_manufacturers = st.sidebar.multiselect("Manufacturer", manufacturers, default=manufacturers)

filtered = df[
    df["year"].isin(selected_years)
    & df["vehicle_category"].isin(selected_categories)
    & df["manufacturer"].isin(selected_manufacturers)
]

if filtered.empty:
    st.warning("No records match the selected filters. Change the filters to view results.")
    st.stop()

total_sales = int(filtered["annual_sales"].sum())
avg_range = filtered["driving_range_km"].mean()
avg_rating = filtered["customer_rating"].mean()
manufacturer_count = filtered["manufacturer"].nunique()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total annual sales", f"{total_sales:,}")
c2.metric("Average driving range", f"{avg_range:.0f} km")
c3.metric("Average customer rating", f"{avg_rating:.1f}/5")
c4.metric("Manufacturers", manufacturer_count)

st.subheader("Sales and market performance")
left, right = st.columns(2)

sales_by_category = (
    filtered.groupby("vehicle_category", as_index=False)["annual_sales"]
    .sum()
    .sort_values("annual_sales", ascending=False)
)
left.plotly_chart(
    px.bar(sales_by_category, x="vehicle_category", y="annual_sales",
           title="Annual sales by vehicle category", labels={
               "vehicle_category": "Vehicle category", "annual_sales": "Annual sales"
           }),
    use_container_width=True,
)

sales_by_manufacturer = (
    filtered.groupby("manufacturer", as_index=False)["annual_sales"]
    .sum()
    .sort_values("annual_sales", ascending=False)
)
right.plotly_chart(
    px.bar(sales_by_manufacturer, x="manufacturer", y="annual_sales",
           title="Annual sales by manufacturer", labels={
               "manufacturer": "Manufacturer", "annual_sales": "Annual sales"
           }),
    use_container_width=True,
)

st.subheader("Battery technology and driving range")
left, right = st.columns(2)

battery_counts = (
    filtered.groupby("battery_technology", as_index=False)["annual_sales"]
    .sum()
    .sort_values("annual_sales", ascending=False)
)
left.plotly_chart(
    px.pie(battery_counts, names="battery_technology", values="annual_sales",
           title="Sales by battery technology"),
    use_container_width=True,
)

range_by_category = (
    filtered.groupby("vehicle_category", as_index=False)["driving_range_km"]
    .mean()
    .sort_values("driving_range_km", ascending=False)
)
right.plotly_chart(
    px.bar(range_by_category, x="vehicle_category", y="driving_range_km",
           title="Average driving range by category", labels={
               "vehicle_category": "Vehicle category", "driving_range_km": "Range (km)"
           }),
    use_container_width=True,
)

st.subheader("Manufacturing locations and customer ratings")
left, right = st.columns(2)

country_sales = (
    filtered.groupby("manufacturing_country", as_index=False)["annual_sales"]
    .sum()
    .sort_values("annual_sales", ascending=False)
)
left.plotly_chart(
    px.bar(country_sales, x="manufacturing_country", y="annual_sales",
           title="Sales by manufacturing country", labels={
               "manufacturing_country": "Manufacturing country",
               "annual_sales": "Annual sales"
           }),
    use_container_width=True,
)

rating_by_category = (
    filtered.groupby("vehicle_category", as_index=False)["customer_rating"]
    .mean()
    .sort_values("customer_rating", ascending=False)
)
right.plotly_chart(
    px.bar(rating_by_category, x="vehicle_category", y="customer_rating",
           title="Average customer rating by category", range_y=[0, 5],
           labels={"vehicle_category": "Vehicle category", "customer_rating": "Rating (out of 5)"}),
    use_container_width=True,
)

with st.expander("View filtered data"):
    st.dataframe(filtered, use_container_width=True)

st.caption("Note: The included CSV contains illustrative sample data for demonstration. Replace it with verified market data before making business decisions.")
