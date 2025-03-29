import yfinance as yf

def fetch_ticker_price(tickers):
    
    tickers_data = yf.Tickers(' '.join([ticker + '.SA' for ticker in tickers]))
    results = []

    for ticker in tickers:
        ticker_completo = ticker + '.SA'
        try:
            # Obtém o preço atual do ticker
            current_price = tickers_data.tickers[ticker_completo].history(period="1d")['Close'][0]
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
