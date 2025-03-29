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
            results.append({
                'ticker': ticker,
                'curPrc': round(current_price, 2)
            })
        except Exception as e:
            results.append({
                'ticker': ticker,
                'error': f"Erro ao obter dados: {str(e)}"
            })

    return results
