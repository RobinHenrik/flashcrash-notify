import yfinance as yf
import pandas as pd

def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    df = tables[0] # First table is what we need
    # Replace '.' with '-' for yfinance compatibility
    return [symbol.replace('.', '-') for symbol in df['Symbol'].tolist()]


TICKERS = get_sp500_tickers()
DROP_THRESHOLD = 0.05 # 10% drop in stock price
RISE_THRESHOLD = 0.05 # 10% rise in stock price
LOOKBACK_MINUTES = 60 # Lookback period in minutes in which the drop threshold is checked against

def get_latest_price(ticker):
    data = yf.Ticker(ticker).history(period="1d", interval="1m")
    if not data.empty:
        latest_row = data.tail(1)
        return float(latest_row["Close"].iloc[0])
    else:
        return None

def check_price_drop(ticker):
    ticker_obj = yf.Ticker(ticker)
    data = ticker_obj.history(period="2d", interval="1m")
    if data.empty:
        return None, None, None

    latest_price =float(data['Close'].iloc[-1])

    if len(data) > LOOKBACK_MINUTES:
        # Market has been open for more than LOOKBACK_MINUTES
        past_price = float(data['Close'].iloc[-LOOKBACK_MINUTES])
    else:
        # Market has been open for less than LOOKBACK_MINUTES
        # Use yesterday's closing price
        # Find last row where the date is *yesterday* (because after-hours/minute data may be weird)
        yesterday = data.index[-1].normalize() - pd.Timedelta(days=1)
        yday_data = data[data.index.normalize() == yesterday]
        if yday_data.empty:
            return None, None, None
        past_price = float(yday_data['Close'].iloc[-1])

    change = (latest_price - past_price) / past_price
    return latest_price, past_price, change

def print_movement(ticker, latest_price, past_price, change, drop_threshold, rise_threshold):
    separator = "---------------------------------------------------------------------\n"
    if latest_price is None or past_price is None or change is None:
        print(f"Could not retrieve data for {ticker}.\n{separator}")
        return

    if change <= -drop_threshold:
        print(f"MAJOR PRICE DROP:\n"
              f"{ticker}:\n"
              f"Current price: ${latest_price:.2f}\n"
              f"Price from 60 minutes ago/yesterday: ${past_price:.2f}\n"
              f"Change: {change*100:.2f} %\n\n"
              f"{separator}")
    elif change >= rise_threshold:
        print(f"MAJOR PRICE RISE:\n"
              f"{ticker}:\n"
              f"Current price: ${latest_price:.2f}\n"
              f"Price from 60 minutes ago/yesterday: ${past_price:.2f}\n"
              f"Change: {change*100:.2f} %\n\n"
              f"{separator}")
    else:
        print(f"No major movement:\n"
              f"{ticker}:\n"
              f"Current price: ${latest_price:.2f}\n"
              f"Price from 60 minutes ago/yesterday: ${past_price:.2f}\n"
              f"Change: {change*100:.2f} %\n\n"
              f"{separator}")
