import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from cache_decorator import cache_memory
from datetime import datetime
from ticker_data_history import fetch_ticker_history_price
from flask import jsonify

@cache_memory(maxsize=100)
def fetch_proventos(
    papeis_tipos: List[Dict[str, int]], 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None
) -> List[Dict[str, List[Dict[str, str]]]]:
    resultados = []
    
    tickerQuery = '-'.join(item['papel'] for item in papeis_tipos)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201",
        "Accept": "text/html, text/plain, text/css, text/sgml, */*;q=0.01"
    }

    # Converte as strings de data para objetos datetime (se fornecidas)
    start_dt = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

    # Itera por cada item no array papeis_tipos
    for item in papeis_tipos:
        papel = item["papel"]
        tipo = item["tipo"]

        url = f"https://www.fundamentus.com.br/{'fii_' if tipo == 1 else ''}proventos.php?papel={papel}&tipo=2"
        response = requests.get(url, headers=headers)

        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tabela_proventos = soup.find('table', {'id': 'resultado'})

            if tabela_proventos:
                linhas = tabela_proventos.find_all('tr')[1:]  # Ignora o cabeçalho
                
                # Lista para armazenar os proventos de cada papel
                proventos_papel = []

                for linha in linhas:
                    colunas = linha.find_all('td')
                    if colunas:
                        valor = colunas[3 if tipo == 1 else 1].text.strip()
                        data_com = colunas[0].text.strip()
                        data_pagamento_str = colunas[2 if tipo == 1 else 3].text.strip()

                        # Converte a data do pagamento para objeto datetime
                        try:
                            # Formato esperado: dd/mm/yyyy
                            data_pagamento = datetime.strptime(data_pagamento_str, "%d/%m/%Y")
                        except ValueError:
                            continue  # Pula datas inválidas

                        # Verifica se a data está no intervalo (se os filtros foram fornecidos)
                        incluir_provento = True
                        if start_dt or end_dt:
                            incluir_provento = False
                            if start_dt and end_dt:
                                incluir_provento = start_dt <= data_pagamento <= end_dt
                            elif start_dt:
                                incluir_provento = data_pagamento >= start_dt
                            elif end_dt:
                                incluir_provento = data_pagamento <= end_dt

                        if incluir_provento:
                            # TODO descobrir um jeito de trazer o calculo de porcentagem (formula abaixo )
                            # (valor / valor_base) * 100
                            # startEndDate = datetime.strptime(data_com, "%d/%m/%Y").strftime("%Y-%m-%d")
                            # baseValue = fetch_ticker_history_price(tickerQuery, startEndDate, startEndDate)
                            # print(baseValue)
                            proventos_papel.append({
                                "value": valor,
                                "payment_date": data_pagamento_str,  # Mantém o formato original
                                "date_com": data_com,
                            })

                # Adiciona o grupo de proventos para o papel atual
                if proventos_papel:
                    resultados.append({
                        "ticker": papel,
                        "proventos": proventos_papel
                    })
            else:
                print(f"Não foi possível encontrar os dados de proventos para {papel} (tipo {tipo}).")
        else:
            print(f"Erro ao acessar a página para {papel} (tipo {tipo}). Status code: {response.status_code}")

    return resultados
