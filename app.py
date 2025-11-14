import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

# APP CONFIG
st.set_page_config(page_title="Enhanced Stock Market Dashboard", layout="wide")
st.title("📈 Enhanced Stock Market Dashboard")
st.caption("Visualized with Streamlit • Data Source: Parquet Files")

# LOAD DATA
agg1 = pd.read_parquet("data/agg1.parquet")   # Daily avg close by ticker
agg2 = pd.read_parquet("data/agg2.parquet")   # Avg volume by sector
agg3 = pd.read_parquet("data/agg3.parquet")   # Daily returns

# SIDEBAR
st.sidebar.header("🔍 Filter Options")

tickers = sorted(agg1["ticker"].unique())
sectors = sorted(agg2["sector"].unique())

ticker = st.sidebar.selectbox("Select Ticker", tickers)
sector_selected = st.sidebar.multiselect("Filter Sectors", sectors, default=sectors)

dates = pd.to_datetime(agg1["trade_date"])
start_date = st.sidebar.date_input("Start Date", dates.min())
end_date = st.sidebar.date_input("End Date", dates.max())

# 🔧 FIX: Convert date_input() output (Python date) → pandas datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# DATA FILTERING
filtered = agg1[
    (agg1["ticker"] == ticker)
    & (pd.to_datetime(agg1["trade_date"]) >= start_date)
    & (pd.to_datetime(agg1["trade_date"]) <= end_date)
]

sector_data = agg2[agg2["sector"].isin(sector_selected)]
returns = agg3[agg3["ticker"] == ticker].sort_values("trade_date")

# MAIN TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📉 Price Trend", "📊 Sector Analysis", "📈 Returns", "📦 Ticker Comparison", "🔥 Correlation Heatmap"
])


# ---------------------- TAB 1: PRICE TREND --------------------------
with tab1:
    st.subheader(f"Price Trend for {ticker}")

    # Area chart
    area_chart = (
        alt.Chart(filtered)
        .mark_area(opacity=0.4, color="#4c78a8")
        .encode(
            x=alt.X("trade_date:T", title="Date"),
            y=alt.Y("close_price:Q", title="Avg Close Price"),
        )
        .properties(height=350)
    )
    st.altair_chart(area_chart, use_container_width=True)

    # Candlestick chart (simulated OHLC)
    st.subheader(f"Candlestick Chart (Simulated OHLC) for {ticker}")

    filtered["open"] = filtered["close_price"] * 0.98
    filtered["high"] = filtered["close_price"] * 1.03
    filtered["low"] = filtered["close_price"] * 0.97

    fig_candle = go.Figure(
        data=[
            go.Candlestick(
                x=filtered["trade_date"],
                open=filtered["open"],
                high=filtered["high"],
                low=filtered["low"],
                close=filtered["close_price"],
                increasing_line_color="green",
                decreasing_line_color="red",
            )
        ]
    )
    fig_candle.update_layout(height=350)
    st.plotly_chart(fig_candle, use_container_width=True)


# ---------------------- TAB 2: SECTOR ANALYSIS -----------------------
with tab2:
    st.subheader("Sector Volume Comparison (Horizontal Bar)")

    bar_chart = (
        alt.Chart(sector_data)
        .mark_bar(color="#72B7B2")
        .encode(
            y=alt.Y("sector:N", sort="-x"),
            x=alt.X("volume:Q", title="Avg Volume"),
        )
        .properties(height=350)
    )
    st.altair_chart(bar_chart, use_container_width=True)

    st.subheader("Treemap of Sector Volume Share")
    fig_tree = px.treemap(
        sector_data,
        path=["sector"],
        values="volume",
        color="volume",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_tree, use_container_width=True)


# ---------------------- TAB 3: RETURNS -------------------------------
with tab3:
    st.subheader(f"Daily Returns Distribution for {ticker}")

    fig_box = px.box(
        returns,
        y="daily_return",
        points="all",
        title="Distribution of Daily Returns"
    )
    st.plotly_chart(fig_box, use_container_width=True)

    st.subheader("Daily Returns Scatter Chart")
    fig_scatter = px.scatter(
        returns,
        x="trade_date",
        y="daily_return",
        color="daily_return",
        color_continuous_scale="RdBu",
        title="Volatility Over Time"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


# ---------------------- TAB 4: MULTI-TICKER COMPARISON ----------------
with tab4:
    st.subheader("Comparison of Average Close Price Across Tickers")

    compare = agg1.groupby(["trade_date", "ticker"], as_index=False)["close_price"].mean()

    fig_multi = px.line(
        compare,
        x="trade_date",
        y="close_price",
        color="ticker",
        title="Daily Avg Close (Smoothed)",
        line_shape="spline"
    )
    st.plotly_chart(fig_multi, use_container_width=True)


# ---------------------- TAB 5: CORRELATION HEATMAP ---------------------
with tab5:
    st.subheader("Ticker Correlation Heatmap")

    pivot = agg1.pivot_table(
        index="trade_date",
        columns="ticker",
        values="close_price"
    )
    corr = pivot.corr().fillna(0)

    fig_heatmap = px.imshow(
        corr,
        color_continuous_scale="Bluered",
        aspect="auto",
        title="Correlation Heatmap of Tickers",
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
