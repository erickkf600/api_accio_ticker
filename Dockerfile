# Use uma imagem base do Python
FROM python:3

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos da aplicação para o contêiner
COPY . .

# Expõe a porta em que a aplicação estará rodando
EXPOSE 4444

# Comando para rodar a aplicação
CMD ["gunicorn", "main:app"]
