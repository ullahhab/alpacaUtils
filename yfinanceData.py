import yfinance as yf
import pandas as pd
from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv


def getNews(symbol):
    ticker = yf.Ticker(symbol)
    news = ticker.news
    for item in news:
        content = item['content']
        date = datetime.fromisoformat(content['pubDate'])
        print(content)
        #print(f"Date: {date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Title: {content['title']}")
        print(f"Publisher: {content['provider']['displayName']}")
        print(f"Description: {content['description']}")

def getEarningsData(symbol):
    ticker = yf.Ticker(symbol)
    earnings = ticker.income_stmt
    estimated_earnings = ticker.earnings_estimate
    earning_dates = ticker.earnings_dates
    print(f"Annual Earning : {earnings}\nEstimated earnings: {estimated_earnings}\nEarning dates{earning_dates}")
    return earnings, estimated_earnings, earning_dates
    
def connectWithgenAI(prompt="Explain how AI works?", model="gemini-2.5-flash"):
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)
    print(response.text)
    

if __name__ =="__main__":
    earnings, estimated_earnings, earning_dates = getEarningsData("AAPL")
    prompt=f"""You are a analyst and I'm providing you with the data of the stock. 
    The data includes earning reports and earning dates. Based on the price of this stock today and looking at financials, do you think the stock will go up or down
    financial data: earning = {earnings}\nEstimated earnings: {estimated_earnings}\nEarning dates{earning_dates}
    response should be in json format and all of that should be in this format: stock: symbol, willGoUp: boolean, reason: reasining summary"""
    connectWithgenAI(prompt=prompt)