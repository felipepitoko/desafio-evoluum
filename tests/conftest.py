# app/tests/conftest.py
import pytest
import psycopg2
from psycopg2.extensions import connection
from fastapi.testclient import TestClient

# Importa as variáveis de configuração separadas para o banco de dados de teste
from config import (
    TEST_POSTGRES_DB,
    TEST_POSTGRES_HOST,
    TEST_POSTGRES_PASSWORD,
    TEST_POSTGRES_PORT,
    TEST_POSTGRES_USER,
)
from routes.dependencies import get_db_handler
from database.db_config import create_tables
from database.db_handler import DBHandler
from main import app

@pytest.fixture(name="db_handler_test_instance")
def db_handler_test_fixture():
    """
    Fixture que fornece uma conexão com o banco de dados de teste.
    """
    conn = psycopg2.connect(dbname=TEST_POSTGRES_DB,
                            user=TEST_POSTGRES_USER,
                            password=TEST_POSTGRES_PASSWORD,
                            host=TEST_POSTGRES_HOST,
                            port=TEST_POSTGRES_PORT)
    create_tables(conn) # Cria as tabelas antes do teste
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE notes, users RESTART IDENTITY CASCADE;")
        conn.commit()
        
        yield DBHandler(conn)
    finally:
        if conn:
            conn.close()

@pytest.fixture(name="client")
def client_fixture(db_handler_test_instance: DBHandler):
    """
    Fixture que retorna uma instância do TestClient com as dependências sobrescritas.
    """
    # Função que irá injetar a conexão de teste no lugar da original
    def override_get_db_handler():
        yield db_handler_test_instance

    # A chave do dicionário é a função de dependência original
    app.dependency_overrides[get_db_handler] = override_get_db_handler

    with TestClient(app) as client:
        yield client
        
    # Limpa as sobrescritas após o teste para evitar efeitos colaterais
    app.dependency_overrides.clear()