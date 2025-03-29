import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from cache_decorator import cache_memory

@cache_memory(maxsize=100)
def fetch_proventos(papeis_tipos: List[Dict[str, int]], ano: str = None) -> List[Dict[str, List[Dict[str, str]]]]:
    resultados = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201",
        "Accept": "text/html, text/plain, text/css, text/sgml, */*;q=0.01"
    }

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
                        data_pagamento = colunas[2 if tipo == 1 else 3].text.strip()

                        # Verifica se o ano foi passado e se o pagamento é do ano informado
                        if ano:
                            if ano in data_pagamento:
                                proventos_papel.append({
                                    "value": valor,
                                    "payment_date": data_pagamento
                                })
                        else:
                            proventos_papel.append({
                                "value": valor,
                                "payment_date": data_pagamento
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
