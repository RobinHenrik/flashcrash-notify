import datetime
import pytz
import pandas_market_calendars as mcal

def is_market_open(now=None):
    # US/Eastern timezone
    eastern = pytz.timezone("US/Eastern")
    now = now or datetime.datetime.now(eastern)
    nyse = mcal.get_calendar('NYSE')

    # Get current day's schedule
    schedule = nyse.schedule(start_date=now.strftime("%Y-%m-%d"), end_date=now.strftime("%Y-%m-%d"))
    if schedule.empty:
        return False  # Holiday or weekend

    market_open = schedule.iloc[0]['market_open']
    market_close = schedule.iloc[0]['market_close']
    # Both market_open and market_close are tz-aware timestamps
    return market_open <= now <= market_close

'''
eastern = pytz.timezone("US/Eastern")
test_time = eastern.localize(datetime.datetime(2025, 5, 27, 12, 0, 0))
print(is_market_open(test_time))
'''