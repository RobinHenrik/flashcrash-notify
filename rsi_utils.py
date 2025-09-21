import pandas_ta as ta

def calculate_rsi(df, ticker):
    return round(ta.rsi(df[(ticker, "Close")], length=14).iloc[-1], 2)