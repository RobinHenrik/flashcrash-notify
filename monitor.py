import yfinance as yf
import pandas as pd
import numpy as np

def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    df = tables[0] # First table is what we need
    # Replace '.' with '-' for yfinance compatibility
    return [symbol.replace('.', '-') for symbol in df['Symbol'].tolist()]


TICKERS = get_sp500_tickers()
DROP_THRESHOLD = 0.10 # 10% drop in stock price
RISE_THRESHOLD = 0.10 # 10% rise in stock price
LOOKBACK_MINUTES = 60 # Lookback period in minutes in which the drop threshold is checked against


def fetch_sp500_history():
    return yf.download(
        TICKERS,
        period="2d",
        interval="1m",
        group_by="ticker",
        auto_adjust=True,
        threads=True,  # use threading for even more speed
        progress=False
    )

def get_latest_price(ticker):
    data = yf.Ticker(ticker).history(period="1d", interval="1m")
    if not data.empty:
        latest_row = data.tail(1)
        return float(latest_row["Close"].iloc[0])
    else:
        return None

def check_price_drop(all_data, ticker):
    # Handle the case where only one ticker is present (no multi-level columns)
    if ticker not in all_data.columns.get_level_values(0):
        return None, None, None

    data = all_data[ticker].dropna()

    if data.empty:
        return None, None, None

    latest_price =float(data['Close'].iloc[-1])

    # Get the dates for each row, normalized (date only, no time)
    all_dates = data.index.normalize()
    today = all_dates[-1]
    today_indices = np.where(all_dates == today)[0]

    if len(today_indices) > LOOKBACK_MINUTES:
        # Market has been open for more than LOOKBACK_MINUTES
        past_price = float(data['Close'].iloc[-LOOKBACK_MINUTES])
    else:
        # Market has been open for less than LOOKBACK_MINUTES
        # Use the previous trading day's close (i.e., the last row before today)
        # Not enough data for today—use previous trading day's close
        if today_indices[0] == 0:
            return None, None, None  # There is no previous day
        past_price = float(data['Close'].iloc[today_indices[0] - 1])

    change = (latest_price - past_price) / past_price
    return latest_price, past_price, change
