
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from cache_decorator import cache_memory

@cache_memory(maxsize=100)
def fetch_ticker_price_yahoo(tickers):

    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201",
        "Accept": "text/html, text/plain, text/css, text/sgml, */*;q=0.01"
    }
    for ticker in tickers:
        try:
            ticker_completo = ticker + '.SA'
            url = f"https://finance.yahoo.com/quote/{ticker_completo}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # levanta erro se status != 200

            soup = BeautifulSoup(response.text, 'html.parser')
            html_cote = soup.find('span', {'data-testid': 'qsp-price'})

            if html_cote:
                price = float(html_cote.text.strip())
                resultados.append({'ticker': ticker, 'curPrc': price})
            else:
                resultados.append({'ticker': ticker, 'curPrc': None})

        except Exception as e:
            # registra o erro e continua o loop
            print(f"Erro ao processar {ticker}: {e}")
            resultados.append({
                'ticker': ticker,
                'error': f"Erro ao obter dados: {str(e)}"
            })

    return resultados
