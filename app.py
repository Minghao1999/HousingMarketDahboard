import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("global_housing_market_extended.csv")

# Title
st.title("🌍 Global Housing Market Dashboard")

# Sidebar filters
st.sidebar.header("Filter Options")
countries = st.sidebar.multiselect("Select countries", options=df["Country"].unique(), default=["USA", "China", "India"])
years = st.sidebar.slider("Select year range", int(df["Year"].min()), int(df["Year"].max()), (2015, 2021))

# Filter data
filtered_df = df[(df["Country"].isin(countries)) & (df["Year"].between(years[0], years[1]))]

# KPIs
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Avg House Price Index", f"{filtered_df['House Price Index'].mean():.2f}")
col2.metric("Avg Affordability Ratio", f"{filtered_df['Affordability Ratio'].mean():.2f}")
col3.metric("Avg GDP Growth (%)", f"{filtered_df['GDP Growth (%)'].mean():.2f}")

# Line Chart - House Price Trend
st.subheader("🏠 House Price Index Over Time")
fig1 = px.line(filtered_df, x="Year", y="House Price Index", color="Country", markers=True)
st.plotly_chart(fig1, use_container_width=True)

# Bar Chart - Affordability Ratio
st.subheader("💸 Affordability Ratio by Country")
latest_year = filtered_df["Year"].max()
latest_data = filtered_df[filtered_df["Year"] == latest_year]
fig2 = px.bar(latest_data, x="Country", y="Affordability Ratio", color="Country")
st.plotly_chart(fig2, use_container_width=True)



# 地理热图 - 各国平均房价指数
st.subheader("🌍 Average House Price Index by Country (Geographic View)")

# 取选中时间段中每个国家的平均房价指数
avg_price_by_country = (
    filtered_df.groupby("Country")["House Price Index"]
    .mean()
    .reset_index()
)

# 使用 choropleth 绘制世界地图
fig_map = px.choropleth(
    avg_price_by_country,
    locations="Country",
    locationmode="country names",  # 确保使用的是标准国名
    color="House Price Index",
    color_continuous_scale="YlOrRd",
    title="Average House Price Index by Country",
)

st.plotly_chart(fig_map, use_container_width=True)


# Optional: Download data
st.download_button("Download Filtered Data as CSV", data=filtered_df.to_csv(index=False), file_name="filtered_housing_data.csv")

