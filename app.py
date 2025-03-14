import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz  

# Set the title of the app
st.title("Is Soham Working?")

# Define the stock ticker symbol for ITC (NSE)
ticker_symbol = "ITC.NS"

# Get today's and yesterday's date in Indian Standard Time (IST)
ist = pytz.timezone("Asia/Kolkata")
now_ist = datetime.now(ist)
today = now_ist.date()
yesterday = today - timedelta(days=1)

# Fetch last 10 days of data to ensure availability
try:
    stock_data = yf.download(
        ticker_symbol,
        period="10d",
        interval="1d",
        auto_adjust=False
    )
except Exception as e:
    st.error(f"Error fetching stock data: {e}")
    stock_data = None

# Validate stock data
if stock_data is not None and not stock_data.empty:
    stock_data = stock_data.dropna().sort_index()  # Drop NaNs and sort by date
    stock_data.index = pd.to_datetime(stock_data.index)  # Ensure datetime index

    # Ensure "Close" exists and has valid data
    if "Close" in stock_data.columns and not stock_data["Close"].dropna().empty:
        # Try today's data, fallback to yesterday or last available
        today_data = stock_data.get(str(today))
        yesterday_data = stock_data.get(str(yesterday))
        
        if today_data is not None:
            selected_data = today_data
            data_source = f"✅ Using data from today ({today})"
        elif yesterday_data is not None:
            selected_data = yesterday_data
            data_source = f"⚠ Market closed today, using data from yesterday ({yesterday})"
        else:
            selected_data = stock_data.iloc[-1]  # Use last available data
            data_source = f"⚠ No recent data found, using last available data from {selected_data.name.date()}"

        # Extract prices
        opening_price = float(selected_data["Open"])
        latest_price = float(selected_data["Close"])
        stock_return = (latest_price - opening_price) / opening_price

        # ✅ Always plot data from the last 5-10 days
        # st.line_chart(stock_data["Close"].tail(10))

        # Display data source
        st.caption(data_source)

        # Soham status
        if stock_return > 0:
            st.subheader("✅ Soham is working")
        else:
            st.subheader("❌ Soham is not working")
    else:
        st.subheader("⚠ No valid closing prices available.")
else:
    st.subheader("⚠ No trading data available. Please check if the market is closed or the ticker symbol is correct.")
