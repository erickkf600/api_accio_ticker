import yfinance as yf
from cache_decorator import cache_memory

@cache_memory(maxsize=100)
def fetch_ticker_price(tickers):
    
    tickers_data = yf.Tickers(' '.join([ticker + '.SA' for ticker in tickers]))
           
    results = []

    for ticker in tickers:
        ticker_completo = ticker + '.SA'
        try:
            # Obtém o preço atual do ticker
            current_price = tickers_data.tickers[ticker_completo].analyst_price_targets['current']
            if current_price is not None:
                results.append({
                    'ticker': ticker,
                    'curPrc': round(current_price, 2)
                })
            else:     
                print(f"{ticker_completo} não encontrado, pulando...")
        except Exception as e:
            print(f"Erro ao buscar {ticker_completo}: {e}")
            continue

    return results
