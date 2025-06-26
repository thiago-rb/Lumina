import psycopg2
import os

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "escola"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "db"),
    "port": "5432"
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG)