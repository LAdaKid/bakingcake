"""
This module will house all crypto related functions.
"""
import datetime
import requests
import pandas as pd


# Use the v3 CoinGecko API
API_URL = "https://api.coingecko.com/api/v3/"


def fetch_supported_coins():
    """
    This function will fetch all CoinGecko supported coins.

    Returns:
        ticker to name dictionary
    """
    url = f"{API_URL}coins/list"
    response = requests.get(url)
    if response.status_code == 200:
        coins = response.json()
        # Create a mapping between ticker symbols and coin names
        ticker_to_name = {coin['symbol'].upper(): coin['id'] for coin in coins}
        return ticker_to_name
    else:
        print(f"Failed to retrieve list of supported coins: {response.content}")
        return None


def fetch_price_history(ticker, start=None, end=None, days=30):
    """
    This function will fetch the crypto price history given a ticker.

    Note: open / close / change % only works for recent history

    Args:
        ticker (str): ticker symbol in all caps
        start (datetime.date): start date
        end (datetime.date): end date
        days (int): lookback period in days

    Return:
        price history DataFrame
    """
    # Map the ticker to the cryptocurrency name
    name = fetch_supported_coins()[ticker]
    # If both start and end are provided, we ignore the 'days' parameter
    if start and end:
        # Convert datetime to string format "dd-mm-yyyy"
        start_str = start.strftime("%d-%m-%Y")
        end_str = end.strftime("%d-%m-%Y")
        # Fetch historical data for custom date range
        url = (
            f"{API_URL}coins/{name}/market_chart/range?vs_currency=usd"
            f"&from={start.timestamp()}&to={end.timestamp()}")
    else:
        # Fetch historical data for the last 'days' days (default is 30 days)
        url = f"{API_URL}coins/{name}/market_chart?vs_currency=usd&days={days}"
    # Get response and return historical prices
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        converted_data = [(
            datetime.datetime.fromtimestamp(ts / 1000.0), price)
            for ts, price in data['prices']]
        df = pd.DataFrame(converted_data, columns=["datetime", "price"])
        df['date'] = df['datetime'].dt.date
        df['ticker'] = ticker
        # Group by date to find open, close, low, high prices
        grouped = df.groupby('date').agg(
            open=pd.NamedAgg(column='price', aggfunc='first'),
            close=pd.NamedAgg(column='price', aggfunc='last'),
            low=pd.NamedAgg(column='price', aggfunc='min'),
            high=pd.NamedAgg(column='price', aggfunc='max')
        ).reset_index()
        # Calculate percent change
        grouped['changePercent'] = ((grouped['close'] - grouped['open']) / grouped['open']) * 100
        grouped['ticker'] = ticker
        grouped = grouped[["date", "ticker", "open", "close", "low", "high", "changePercent"]]
        
        return grouped
    else:
        return f"Failed to retrieve data: {response.content}"
