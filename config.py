import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do Banco de Dados Principal (usado pela aplicação)
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)

# Configurações do Banco de Dados de Teste (usado pelo pytest)
TEST_POSTGRES_USER = os.getenv("TEST_POSTGRES_USER")
TEST_POSTGRES_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD")
TEST_POSTGRES_DB = os.getenv("TEST_POSTGRES_DB")
TEST_POSTGRES_HOST = os.getenv("TEST_POSTGRES_HOST")
TEST_POSTGRES_PORT = os.getenv("TEST_POSTGRES_PORT", 5433)

# Segredo da Aplicação
SECRET_TOKEN = os.getenv("SECRET_TOKEN")