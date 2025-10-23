import yfinance as yf
import pandas as pd
from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json


def getNews(symbol, printAll=False, volume=0):
    ticker = yf.Ticker(symbol)
    news = ticker.news
    print(type(news))
    if printAll:
        for item in news:
            content = item['content']
            date = datetime.fromisoformat(content['pubDate'])
            print(content)
            #print(f"Date: {date.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Title: {content['title']}")
            print(f"Publisher: {content['provider']['displayName']}")
            print(f"Description: {content['description']}")
    if not volume:
        ret = news[-1] #Just the last one
    else:
        ret = news[-1:-volume-1:-1] #gives news of last volume if number exceeds the list will still the same
    return ret #Just the last one

def getEarningsData(symbol):
    ticker = yf.Ticker(symbol)
    earnings = ticker.income_stmt
    estimated_earnings = ticker.earnings_estimate
    earning_dates = ticker.earnings_dates
    historical_data = ticker.history(period="1d")
    current_price  = historical_data['Close'][0]
    print(f"Annual Earning : {earnings}\nEstimated earnings: {estimated_earnings}\nEarning dates{earning_dates}")
    return earnings, estimated_earnings, earning_dates, current_price
    
def connectWithgenAI(prompt="Explain how AI works?", model="gemini-2.5-flash"):
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)
    print(response.text)
    return response.text
    

if __name__ =="__main__":
    symbol = "IQ"
    earnings, estimated_earnings, earning_dates, current_price = getEarningsData(symbol)
    reach_price = 3
    content = getNews(symbol) # I'm only interested in the last one
    content = content['content']['summary'] if len(content['content']['summary'])!=0 else content['content']['description']
    print(content)
    date = "01/01/2026"
    prompt=f"""You are a analyst and I'm providing you with the data of the stock. 
    The data includes earning reports and earning dates. Based on the price of this stock today and looking at financials, do you think the stock will go up or down. RIght now the price is at {current_price} is it possible to reach {reach_price}. If you have to estimate, when do you think it will go up or down by {date}
    also here is the news: {content}
    financial data: earning = {earnings}\nEstimated earnings: {estimated_earnings}\nEarning dates{earning_dates} stock symbol: {symbol}
    response should be in json format but with text not ```json ``` and enclose it in json braces tag and all of that should be in this format alway make sure you have braces enforced: stock: symbol, willGoUp: boolean, reason: reasoning summary"""
    
    print(prompt)
    while True:
        try:
            data = json.loads(connectWithgenAI(prompt=prompt))
            break
        except Exception as e:
            pass
    print(f"Sock: {data['stock']}\n{"will Go Up" if data['willGoUp'] else "will go down" }\nreason:{data['reason']}")
    