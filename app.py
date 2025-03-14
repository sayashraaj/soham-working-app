import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz  # For timezone conversion

# Set the title of the app
st.title("Is Soham Working?")

# Define the stock ticker symbol for ITC (NSE)
ticker_symbol = "ITC.NS"

# Get today's date in Indian Standard Time (IST)
ist = pytz.timezone("Asia/Kolkata")
now_ist = datetime.now(ist)
today = now_ist.date()

# Fetch stock data for today (adding a buffer day to avoid missing data)
stock_data = yf.download(
    ticker_symbol,
    start=today - timedelta(days=1),  # Fetch from yesterday to avoid missing early morning data
    end=today + timedelta(days=1),
    interval="5m",  # Using 5-minute interval for better accuracy
)

# Check if data is available
if not stock_data.empty:
    # Filter data for today only
    stock_data = stock_data.loc[stock_data.index.date == today]

    if not stock_data.empty:
        # Get the opening and latest price
        opening_price = stock_data["Open"].iloc[0]
        latest_price = stock_data["Close"].iloc[-1]

        # Calculate today's return
        stock_return = (latest_price - opening_price) / opening_price

        # Display the stock trendline
        st.line_chart(stock_data["Close"])

        # Show whether Soham is working or not
        if stock_return > 0:
            st.subheader("✅ Soham is working")
        else:
            st.subheader("❌ Soham is not working")
    else:
        st.subheader("⚠ Market data for today is not yet available. Try again later.")
else:
    st.subheader("⚠ No trading data available.")
