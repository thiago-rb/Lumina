FROM postgres:latest

# definindo variaveis de ambiente
ENV POSTGRES_DB=escola
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_INITDB_ARGS="--encoding=UTF8"

# copiando o arquivo de inicialização SQL
COPY init.sql /docker-entrypoint-initdb.d/