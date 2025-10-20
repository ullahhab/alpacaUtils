import alpaca_trade_api as tradeapi 
from alpaca_trade_api.rest import APIError
import os
from dotenv import load_dotenv

def checkAlpacaConnection(url=None, secret=None, key=None):
    try:
        client = buildClient(url=url, secret=secret, key=key)
        account = client.get_account()
        return client
    except tradeapi.rest.APIError as e:
        print("Connection error: ", e)
        return None
    except Exception as e:
        print("Somethign went wrong", e)
        return None

def buildClient(url=None, secret=None, key=None):
    client = tradeapi.REST(key, secret_key=secret, base_url=url)
    return client

def getAllStock(client):
    return client.list_assets(status='active')
def getOptionsStock(client):
    stocks = getAllStock(client)
    #return stocks[0]
    #return client.get_asset('AAPL').attributes
    return {a.symbol:a.name for a in stocks if 'has_options' in a.attributes}

def writeKey(url, key, secret):
    client = checkAlpacaConnection(url, secret, key)
    while client == None:         
       print("Please try again: ")
       key = input("Please input ALPACA Key: ")
       secret = input("please input ALPACA Secrets: ")
       url = input("Please input url for credentials: ")
       client = checkAlpacaConnection(url, secret, key)
    #write to dotenv file
    with open('.env', 'w') as env_file:
        env_file.write(f"ALPACA_API_KEY={key}\nALPACA_SECRET_KEY={secret}\nALPACA_URL={url}")
    print(f"Credentials has been written to the file")
    return client

if __name__ == "__main__":
    client = ""
    if '.env' not in os.listdir():
        key = input("Please input ALPACA Key: ")
        secret = input("please input ALPACA Secrets: ")
        url = input("Please input url for credentials: ")
    else:
        load_dotenv()
        key = os.getenv("ALPACA_API_KEY")
        secret = os.getenv("ALPACA_SECRET_KEY")
        url = os.getenv("ALPACA_URL")
        print(key, secret, url)

    client = writeKey(url, key, secret)
    stocks = getOptionsStock(client)
    for stock in stocks:
        print(f"{stock} : {stocks[stock]}")
        
    
    
     