from cache_decorator import cache_memory
import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
from datetime import datetime


@cache_memory(maxsize=100)
def fetch_ticker_history_price(tickers, start_date: str, end_date: str):
    resultados = []
    if not start_date or not end_date:
        raise ValueError("Necessário inserir data de inicio e fim")
    if start_date > end_date:
        raise ValueError("A data de início não pode ser posterior à data final")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201",
        "Accept": "text/html, text/plain, text/css, text/sgml, */*;q=0.01"
    }
    for ticker in tickers:
        try:
            ticker_completo = ticker + '.SA'
            url = f"https://finance.yahoo.com/quote/{ticker_completo}/history"
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # levanta erro se status != 200

            soup = BeautifulSoup(response.text, 'html.parser')
            tabela = soup.find('table', {'class': 'yf-1jecxey'})
            if tabela:
                linhas = tabela.find_all('tr')[1:]
                historico = []
                for linha in linhas:
                    colunas = linha.find_all('td')
                    if colunas:
                        date = datetime.strptime(colunas[0].text.strip(), "%b %d, %Y")
                        formatted_date = date.strftime("%Y-%m-%d")
                        filtrar = start_date <= formatted_date <= end_date

                        if filtrar:     
                            historico.append({
                                "valor": colunas[4].text.strip(),
                                "data": formatted_date
                            })
                            
                if historico: 
                    resultados.append(historico)
                
        except Exception as e:
            # registra o erro e continua o loop
            print(f"Erro ao processar {ticker}: {e}")
            resultados.append({
                'ticker': ticker,
                'error': f"Erro ao obter dados: {str(e)}"
            })

    return resultados



# def fetch_ticker_history_price(tickers):
    
#     # CASO QUEIRO EXIBIR SOMENTE DE UM DIA: A Data final deve ser +1 da data inicio
#     # EX: start='2025-07-31', end='2025-08-01'
    # start_date = "2025-08-14"
    # end_date = "2025-08-14"
#     tickers_sa = [ticker + ".SA" for ticker in tickers]
#     results = []
#     try:
#         tickers_data = yf.Tickers(' '.join([ticker + '.SA' for ticker in tickers]))
#         his = tickers_data.history(period='1mo')
#         # for ticker in tickers_sa:
#         #     price = his.tickers[ticker_completo].analyst_price_targets['current']
#         #     results.append({
#         #         'ticker': ticker,
#         #         'curPrc': round(current_price, 2)
#         #     })
#     except Exception as e:
#         return  results.append({
#                 'error': f"Erro ao obter dados: {str(e)}"
#             })

#     # # Baixa os dados históricos no intervalo de datas
#     # df = yf.download(
#     #     tickers=tickers_sa,
#     #     start=start_date,
#     #     end=end_date,
#     #     group_by="ticker"
#     # )
#     # return df
#     # df_close = df.loc[:, df.columns.get_level_values(1) == 'Close']
#     # ultimo_close = df_close.iloc[-1]
#     # print(ultimo_close)
    
#     # df_dict = df.to_dict(orient="index")

#     # return df_dict
#     # tickers_data = yf.Tickers(' '.join([ticker + '.SA' for ticker in tickers]))
#     # history_data = tickers_data.history()
#     # resultado = {}
#     # for ticker in tickers:
#     #     ticker_completo = ticker + '.SA'
#     #     df =  tickers_data.tickers[ticker_completo].history()
#     #     historico_lista = [
#     #         {
#     #             "data": index.strftime("%Y-%m-%d"),
#     #             "abertura": round(row["Open"], 2),
#     #             "fechamento": round(row["Close"], 2),
#     #             "alta": round(row["High"], 2),
#     #             "baixa": round(row["Low"], 2),
#     #             "volume": int(row["Volume"])
#     #         }
#     #         for index, row in df.iterrows()
#     #     ]
#     #     resultado[ticker] = historico_lista
#     # return resultado
    

#     # for ticker in tickers:
#     #     ticker_completo = ticker + '.SA'

#     #     try:
#     #         # Obtém o preço atual do ticker
#     #         current_price = tickers_data.tickers[ticker_completo].analyst_price_targets['current']
#     #         print(current_price)
#             # results.append({
#             #     'ticker': ticker,
#             #     'curPrc': round(current_price, 2)
#             # })
#     #     except Exception as e:
#     #         print(f"Erro ao processar {ticker}: {e}")
#     #         results.append({
#     #             'ticker': ticker,
#     #             'error': f"Erro ao obter dados: {str(e)}"
#     #         })

#     # return results

