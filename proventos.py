import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
from cache_decorator import cache_memory
from datetime import datetime, timedelta
from ticker_data_history import fetch_ticker_history_price

# Função para parsear a tabela de proventos
def parse_proventos(html: str, start_dt: datetime, end_dt: datetime, papel: str) -> List[Dict]:
    soup = BeautifulSoup(html, "lxml")
    tabela = soup.find("table", id="resultado")
    if not tabela or not tabela.tbody:
        return []

    proventos = []
    linhas = tabela.tbody.find_all("tr")
    
    for linha in linhas:
        cols = [td.text.strip() for td in linha.find_all("td")]
        if len(cols) != 4:
            continue

        data_com_str, tipo_str, data_pag_str, valor_str = cols

        try:
            data_pag = datetime.strptime(data_pag_str, "%d/%m/%Y")
        except ValueError:
            continue

        if not (start_dt <= data_pag <= end_dt):
            continue

        try:
            startDate = datetime.strptime(data_com_str, "%d/%m/%Y").strftime("%Y-%m-%d")
            endDate = (datetime.strptime(data_com_str, "%d/%m/%Y") + timedelta(days=1)).strftime("%Y-%m-%d")
            baseValue = fetch_ticker_history_price([papel], startDate, endDate)
            valor_base_str = baseValue[0]["valores"][0]["valor"]
            valor_base_float = float(valor_base_str.replace(",", "."))
            valor_float = float(valor_str.replace(",", "."))
            percentual = (valor_float / valor_base_float) * 100
        except Exception:
            percentual = 0.0

        proventos.append({
            "value": valor_float,
            "payment_date": data_pag_str,
            "date_com": data_com_str,
            "percent": f"{percentual:.2f}"
        })

    return proventos

# Função para buscar proventos de um ticker
async def fetch_papel(session: aiohttp.ClientSession, papel: str, tipo: int, start_dt: datetime, end_dt: datetime) -> Dict:
    url = f"https://www.fundamentus.com.br/{'fii_' if tipo == 1 else ''}proventos.php?papel={papel}&tipo=2"
    proventos_papel = []

    try:
        async with session.get(url, timeout=20) as response:
            html = await response.text()
            proventos_papel = parse_proventos(html, start_dt, end_dt, papel)
    except Exception as e:
        print(f"Erro ao processar {papel}: {e}")

    return {"ticker": papel, "proventos": proventos_papel}

# Função principal assíncrona
async def fetch_proventos_async(
    papeis_tipos: List[Dict[str, int]],
    start_date: str,
    end_date: str
) -> List[Dict]:
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    async with aiohttp.ClientSession(headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }) as session:
        tasks = [
            fetch_papel(session, item["papel"], item["tipo"], start_dt, end_dt)
            for item in papeis_tipos
        ]
        resultados = await asyncio.gather(*tasks)
    return resultados

@cache_memory(maxsize=100)
def fetch_proventos(
    papeis_tipos: List[Dict[str, int]],
    start_date: str,
    end_date: str
) -> List[Dict]:
    return asyncio.run(fetch_proventos_async(papeis_tipos, start_date, end_date))
