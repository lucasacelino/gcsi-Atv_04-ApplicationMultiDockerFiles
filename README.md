# Atividade 04 da disciplina de Gerência e Configuração de Serviços para Internet

Esta ativdade tem como objetivo criar dois Dockerfiles:

- Um para executar a aplicação backend com Flask
- um para executar o banco de dados Postgres

# 1ª etapa - criar uma rede docker para que tenha uma comunicação entre os dados do contêiner:
`docker network create flask-network`

# 1ª etapa - criar o Dockerfile do SGBD Postgres:
```
FROM postgres:16

COPY init.sql /docker-entrypoint-initdb.d/
```

- O `FROM` importa a imagem do Postgres que está no Dockerhub.
- O `COPY` copia o arquivo init.sql que foi definido na pasta `/postgres` referenciando o docker-entrypoint-initdb.d/(quando o contêiner for inicializado, executa a declaração fornecida no init.sql) 

## Criar a imagem do banco de dados:
`docker build -t db-postgres ./postgres`

## Criar o contêiner de execução do SGBD:
```
docker run -d \
  --name pg-container \
  --network flask-network \
  -p 5433:5432 \
  -e POSTGRES_DB=pedidos \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=123 \
  db-postgres
```
Agora o contêiner do SGBD já está em execução!

# 2ª etapa- criar o Dockerfile da aplicação backend Flask:
```
FROM python:3.11-slim

WORKDIR /app

COPY app/ .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]

```

## Criar a imagem da aplicação:
`docker build -t flaskapp -f Dockerfile.flaskapp .`

## Criar o contêiner da aplicação:
```
docker run -p 5000:5000 \
  --name flask-container \
  --network flask-network \
  -e DB_HOST=pg-container \
  -e DB_PORT=5432 \
  -e DB_NAME=pedidos \
  -e DB_USER=postgres \
  -e DB_PASSWORD=123 \
  flaskapp
```