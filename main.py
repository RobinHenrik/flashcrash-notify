import yfinance as yf

TICKERS = ["AAPL", "MSFT", "AMZN", "GOOGL"]

def get_latest_price(ticker):
    data = yf.Ticker(ticker).history(period="1d", interval="1m")
    if not data.empty:
        latest_row = data.tail(1)
        return float(latest_row["Close"].iloc[0])
    else:
        return None

def main():
    for ticker in TICKERS:
        price = get_latest_price(ticker)
        if price:
            print(f"{ticker}: ${price:.2f}")
        else:
            print(f"{ticker}: Price not found")

if __name__ == "__main__":
    main()

