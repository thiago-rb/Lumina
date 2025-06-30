import psycopg2
import os
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "escola"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "db"),
    "port": os.getenv("DB_PORT", "5432")
}

def connect_db():
    """Estabelece conexão com o banco PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        raise

def get_db_cursor(conn):
    """Retorna cursor com formato de dicionário para facilitar uso"""
    return conn.cursor(cursor_factory=RealDictCursor)