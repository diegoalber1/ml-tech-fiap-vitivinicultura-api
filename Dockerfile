# Usar a imagem base do Python 3.12 com Alpine
FROM python:3.12-alpine

# Definir diretório de trabalho no contêiner
WORKDIR /app

# Copiar o arquivo de requisitos para o contêiner
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação para o contêiner
COPY ./app ./app

# Expor a porta que a aplicação usará
EXPOSE 8000

# Definir o comando de entrada
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
