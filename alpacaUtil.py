import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import APIError
import os
from dotenv import load_dotenv

def buildClient(url: str = None, secret: str = None, key: str = None) -> tradeapi.REST:
    """
    Builds and returns an Alpaca REST client.

    Args:
        url (str): Base URL of the Alpaca API.
        secret (str): Alpaca secret key.
        key (str): Alpaca API key.

    Returns:
        tradeapi.REST: Configured Alpaca REST client.
    """
    client = tradeapi.REST(key, secret_key=secret, base_url=url)
    return client


def checkAlpacaConnection(url=None, secret=None, key=None) -> tradeapi.REST | None:
    """
    Checks connection to Alpaca account.

    Args:
        url (str): Base URL of the Alpaca API.
        secret (str): Alpaca secret key.
        key (str): Alpaca API key.

    Returns:
        tradeapi.REST | None: Returns client if connection successful, else None.
    """
    try:
        client = buildClient(url=url, secret=secret, key=key)
        account = client.get_account()
        return client
    except APIError as e:
        print("Connection error:", e)
        return None
    except Exception as e:
        print("Something went wrong:", e)
        return None


def getAllStock(client: tradeapi.REST) -> list:
    """
    Returns a list of all active stocks from Alpaca.

    Args:
        client (tradeapi.REST): Alpaca REST client.

    Returns:
        list: List of Alpaca Asset objects.
    """
    return client.list_assets(status='active')


def getOptionsStock(client: tradeapi.REST, printable: bool = False) -> dict:
    """
    Looks up optionable stocks tradable on Alpaca account.

    Args:
        client (tradeapi.REST): Alpaca REST client.
        printable (bool): If True, prints the symbol:name mapping.

    Returns:
        dict: Dictionary of optionable stocks {symbol: name}.
    """
    stocks = getAllStock(client)
    optionsStocks = {a.symbol: a.name for a in stocks if 'has_options' in a.attributes}
    if printable:
        for symbol, name in optionsStocks.items():
            print(f"{symbol} : {name}")
    return optionsStocks


def getLatestTrades(client: tradeapi.REST, symbol: str, limit: int = 10) -> list:
    """
    Fetches the latest trades for a given stock symbol.

    Args:
        client (tradeapi.REST): Alpaca REST client.
        symbol (str): Stock symbol to fetch trades for.
        limit (int): Number of latest trades to fetch.

    Returns:
        list: List of latest trades (each trade contains price, size, timestamp).
    """
    trades = client.get_trades(symbol, limit=limit)
    return [{"price": t.price, "size": t.size, "timestamp": t.timestamp} for t in trades]


def writeKey(url: str, key: str, secret: str) -> tradeapi.REST:
    """
    Writes Alpaca API credentials to .env file after verifying the connection.

    Args:
        url (str): Alpaca base URL.
        key (str): Alpaca API key.
        secret (str): Alpaca secret key.

    Returns:
        tradeapi.REST: Verified Alpaca REST client.
    """
    url = url.split('/v')[0]  # Remove version from URL if present
    client = checkAlpacaConnection(url, secret, key)
    while client is None:
        print("Please try again:")
        key = input("Please input ALPACA Key: ")
        secret = input("Please input ALPACA Secret: ")
        url = input("Please input URL for credentials: ")
        client = checkAlpacaConnection(url, secret, key)

    # Write to .env file
    with open('.env', 'w') as env_file:
        env_file.write(f"ALPACA_API_KEY={key}\nALPACA_SECRET_KEY={secret}\nALPACA_URL={url}\n")

    print("Credentials have been written to the file")
    return client


if __name__ == "__main__":
    client = None
    if '.env' not in os.listdir():
        key = input("Please input ALPACA Key: ")
        secret = input("Please input ALPACA Secret: ")
        url = input("Please input URL for credentials: ")
    else:
        load_dotenv()
        key = os.getenv("ALPACA_API_KEY")
        secret = os.getenv("ALPACA_SECRET_KEY")
        url = os.getenv("ALPACA_URL")

    client = writeKey(url, key, secret)
    stocks = getOptionsStock(client, printable=True)

    # Example usage of latest trades
    if stocks:
        symbol = list(stocks.keys())[0]  # Take first optionable stock
        latest_trades = getLatestTrades(client, symbol)
        print(f"\nLatest trades for {symbol}:")
        for trade in latest_trades:
            print(trade)
