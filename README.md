# flashcrash-notify

**flashcrash-notify** is a Python tool for monitoring S&P 500 stock prices in real-time using [yfinance](https://github.com/ranaroussi/yfinance). It detects rapid price drops or rises (10%+ in a short period) and sends instant Telegram alerts, helping you spot potential market overreactions.

## Features

- Monitors selected S&P 500 tickers at regular intervals
- Detects price movements exceeding ±10% within 60 minutes (customizable)
- Sends alerts to a Telegram group or user
- Modular, easy-to-extend codebase

## Setup

1. **Clone the repository and install requirements:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Create a `.env` file in the project root directory** (do **not** commit this file to GitHub as it contains sensitive credentials):

    ```
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    TELEGRAM_GROUP_ID=your_group_or_chat_id
    ```

    - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from BotFather  
    - `TELEGRAM_GROUP_ID`: The chat ID or group ID where you want alerts sent

3. **Run the notifier:**
    ```bash
    python main_notify.py
    ```

    The script will check price changes for the tickers specified in `monitor.py` and send Telegram alerts for significant movements.

## Disclaimer

This tool is intended for personal use and educational or informational purposes only. It does **not** constitute financial advice. Please do your own research before making any investment decisions.
