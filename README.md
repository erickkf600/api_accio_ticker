# 📈 API de Consulta de Proventos e Preços de Tickers  

Esta API foi desenvolvida para obter informações financeiras, como **proventos** de ativos e **preços atuais** de tickers da B3, utilizando dados do **Fundamentus** e **Yahoo Finance**.  

## 🚀 Funcionalidades  

- 📊 **Consultar proventos** (dividendos e juros sobre capital próprio) de ações e FIIs.  
- 💰 **Obter o preço atual** de múltiplos tickers da bolsa brasileira (B3).  

---

## ⚙️ **Como Executar**

1️⃣ **Clone o repositório:**  
```bash
git clone https://github.com/erickkf600/api_accio_ticker.git
cd api_accio_ticker
```
2️⃣ **Crie um ambiente virtual (opcional):**  
```bash
python -m venv venv # Caso seja python3: python3 -m venv venv
source venv\Scripts\activate  # No Linux/Mac: source venv/bin/activate
```

3️⃣ **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4️⃣ **Inicie a API:**
```bash
python main.py
```

## 🚀 Executando em Produção  

Para rodar a API em um ambiente de produção, utilize um servidor WSGI como **Gunicorn**.

```bash
gunicorn main:app
```

### 1️⃣ Instale o Gunicorn (se ainda não tiver)  

## 🔗 **Rotas Disponíveis**  

### 📌 **1. Obter Proventos**  

**Endpoint:**  
```
 POST /proventos
```
**Descrição:**  
Consulta os proventos (dividendos, JCP) de ativos da B3 com base nos tickers informados.  

**Parâmetros (JSON no corpo da requisição):**  
```json
{
    "ano": 2024,
    "papeis_tipos": [
        {"papel": "MXRF11", "tipo": 1},
        {"papel": "PETR4", "tipo": 2}
    ],
}
```

* `papel`: Código do ativo na B3 (ex: "MXRF11", "PETR4").
* `tipo`: 1 para FIIs, 2 para ações.
* `ano (opcional)`: Filtro para um ano específico.

**Exemplo de Resposta:** 
```json
[
    {
        "ticker": "MXRF11",
        "proventos": [
            {
                "payment_date": "13/12/2024",
                "value": "0,10"
            }
        ]
    },
    {
        "ticker": "PETR4",
        "proventos": [
            {
                "payment_date": "23/12/2024",
                "value": "1,5517"
            }
        ]
    }
]
```


### 📌 **2. Obter Preço Atual de Tickers**

**Endpoint:**  
```
 GET /ticker?ticker=MXRF11-HGLG11-PETR4
```
**Descrição:**  
Obtém o preço atual de múltiplos tickers, utilizando dados do Fundamentus. 

**Parâmetro:**  

`ticker` → Lista de tickers separados por `-`.

**Exemplo de Resposta:** 
```json
[
    {
        "ticker": "MXRF11",
        "curPrc": 9.13
    },
    {
        "ticker": "HGLG11",
        "curPrc": 150.75
    },
    {
        "ticker": "PETR4",
        "curPrc": 30.10
    }
]
```

## Responsável

<table>
  <tr>
    <td align="center">
      <a href="#">
        <img src="https://avatars3.githubusercontent.com/u/35529628" width="100px;" alt="Foto do Erick Ferreira no GitHub"/><br>
        <sub>
          <b>Erick Ferreira</b>
        </sub>
      </a>
    </td>
  </tr>
</table>