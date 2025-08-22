from cache_decorator import cache_memory
import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
from datetime import datetime
import json


@cache_memory(maxsize=100)
def fetch_ticker_history_price(tickers, start_date: str, end_date: str):
    tickers_sa = [ticker + ".SA" for ticker in tickers]
    if not start_date or not end_date:
        raise ValueError("Necessário inserir data de inicio e fim")
    if start_date > end_date:
        raise ValueError("A data de início não pode ser posterior à data final")
    
    df = yf.download(tickers_sa, start=start_date, end=end_date, auto_adjust=False)
    
    # Pega só o Close e reseta o índice (pra ter a coluna Date)
    close_df = df["Close"].reset_index()
    close_df["Date"] = close_df["Date"].dt.strftime("%Y-%m-%d")
    
    result = [
        {
            "ticker": ticker.replace(".SA", ""),
            "valores": [
            {
                "data": row["Date"],
                "valor": f"{0 if pd.isna(row[ticker]) else row[ticker]:.2f}"
            }
            for _, row in close_df.iterrows()
        ]
        }
        for ticker in close_df.columns if ticker != "Date"
    ]
    
    return result

