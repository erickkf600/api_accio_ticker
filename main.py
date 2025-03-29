from flask import Flask, request, jsonify
from proventos import fetch_proventos
from ticker_data import fetch_ticker_price

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/', methods=['GET'])
def works_api(): 
    return 'API TICKER WORKS'

@app.route('/proventos', methods=['POST'])
def get_proventos_api():
    try: 
        request_data  = request.get_json()
        
        # Verifica se 'papeis_tipos' está presente no corpo da requisição
        if 'papeis_tipos' not in request_data:
            return jsonify({"error": "A requisição deve conter um JSON com a chave 'papeis_tipos'"}), 400
        
        data = request_data['papeis_tipos']
        # Valida se 'data' é uma lista
        if not data or not isinstance(data, list):
            return jsonify({"error": "A chave 'papeis_tipos' deve conter uma lista de objetos {papel, tipo}"}), 400
        
        # Verificando se todos os objetos possuem as chaves 'papel' e 'tipo'
        for item in data:
            if not isinstance(item, dict):
                return jsonify({"error": "Cada item na lista deve ser um objeto (dict)."}), 400
            
            if 'papel' not in item or 'tipo' not in item:
                return jsonify({"error": "Cada objeto deve conter as chaves 'papel' e 'tipo'."}), 400
            
            if not isinstance(item['papel'], str):
                return jsonify({"error": "A chave 'papel' deve ser uma string."}), 400
            
            if not isinstance(item['tipo'], int):
                return jsonify({"error": "A chave 'tipo' deve ser um número inteiro (1 ou 2)."}), 400

        # Recupera o ano (opcional)
        ano = request_data.get('ano')
        resultado = fetch_proventos(data, ano)
        return jsonify(resultado), 200
    
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tickers', methods=['GET'])
def get_tickers_api(): 
    try:
        raw_tickers = request.args.get("ticker", "")
        
        if not raw_tickers:
            return jsonify({"error": "A requisição deve conter pelo menos um ticker no parâmetro 'ticker'."}), 400

         # Divide os tickers corretamente
        tickers = raw_tickers.split("-")
        
        resultado = fetch_ticker_price(tickers)
        return jsonify(resultado), 200
    
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        


app.run()
