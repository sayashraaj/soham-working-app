import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Set the title of the app
st.title("Is Soham Working?")

# Define the stock ticker symbol for ITC (NSE)
ticker_symbol = 'ITC.NS'

# Get today's date
today = datetime.now().date()

# Fetch stock data for today (intraday prices)
stock_data = yf.download(ticker_symbol, start=today, end=today + timedelta(days=1), interval='1m')

# Check if data is available
if not stock_data.empty:
    # Get the opening and latest price
    opening_price = stock_data['Open'][0]  # First price of the day
    latest_price = stock_data['Close'].iloc[-1]  # Most recent price

    # Calculate today's return
    stock_return = (latest_price - opening_price) / opening_price

    # Display the stock trendline
    st.line_chart(stock_data['Close'])

    # Show whether Soham is working or not
    if stock_return > 0:
        st.subheader("✅ Soham is working")
    else:
        st.subheader("❌ Soham is not working")
else:
    st.subheader("⚠ No trading data available for today.")
