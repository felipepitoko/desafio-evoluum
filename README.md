# App de Notas com FastAPI e Docker

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100-green.svg)
![Docker](https://img.shields.io/badge/Docker-24.0-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Este é um projeto de um aplicativo de notas simples, desenvolvido com um backend em FastAPI, um banco de dados PostgreSQL e um frontend em HTML, CSS e JavaScript puro. Toda a aplicação é orquestrada com Docker e Docker Compose.

Conceitos utilizados:
1. FastAPI como ferramenta para construção rápida de aplicações.
2. Postgres como um banco de dados relacional completo, porém muito fácil de utilizar.
3. Autenticação via token como solução de segurança prática.
4. O valor da arquitetura em camadas , especialmente o padrão Controller-Service-Repository para mantenebilidade do código.


O token utilizado na documentação não tem encriptação nenhuma, sendo apenas demonstrativo e servindo no máximo para separar as notas de cada usuário.

## Funcionalidades

- **Backend API**: Uma API RESTful robusta construída com FastAPI.
- **Frontend Simples**: Uma interface web para interação do usuário, servida diretamente pelo FastAPI.
- **Autenticação**: Sistema de login por usuário baseado em token.
- **Operações CRUD**: Funcionalidades completas para Criar, Ler, Atualizar e Apagar notas.
- **Ambiente Containerizado**: Configuração completa com Docker Compose para os serviços de API, banco de dados e Adminer.
- **Gerenciador de Banco de Dados**: Inclui o Adminer para fácil visualização e gerenciamento do banco de dados.

## Pré-requisitos

Para executar este projeto, você precisará ter instalado em sua máquina:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Como Executar

Siga os passos abaixo para configurar e executar a aplicação em seu ambiente local.

### 1. Clone o Repositório

```sh
git clone <url-do-seu-repositorio>
cd desafio-evoluum
```

### 2. Configure as Variáveis de Ambiente

Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env`.

```sh
# No Linux ou macOS
cp .env.example .env

# No Windows
copy .env.example .env
```

Você pode customizar as variáveis dentro do arquivo `.env` se desejar, mas os valores padrão são suficientes para o ambiente de desenvolvimento.

### 3. Suba os Containers

Com o Docker em execução, utilize o Docker Compose para construir as imagens e iniciar todos os containers.

```sh
docker-compose up --build
```

O comando irá:
1. Construir a imagem Docker para a API.
2. Iniciar o container do banco de dados PostgreSQL.
3. Aguardar o banco de dados ficar pronto.
4. Iniciar o container da API, que primeiro executará o script para criar as tabelas e depois iniciará o servidor.
5. Iniciar o container do Adminer.

## Acessando a Aplicação

Após a inicialização, os serviços estarão disponíveis nos seguintes endereços:

- **Aplicação Web**: http://localhost:8000
  - *A interface principal para criar e gerenciar suas notas.*

- **Documentação da API (Swagger UI)**: http://localhost:8000/docs
  - *Uma interface interativa para visualizar e testar todos os endpoints da API.*

- **Adminer (Gerenciador de Banco de Dados)**: http://localhost:8080
  - *Use as credenciais do seu arquivo `.env` para fazer login (Sistema: `PostgreSQL`, Servidor: `db`, Usuário e Senha).*

  ## Modo de uso
  1. Escolha um nome de usuário (para fins de demonstração, serve apenas para separar as notas de cada usuário)
  2. Crie uma nova nota
  3. Edite ou exclua suas notas criadas

## Executando os Testes

Para executar a suíte de testes automatizados, primeiro instale as dependências de desenvolvimento:

```sh
pip install -r requirements-dev.txt
```

Em seguida, execute o Pytest na raiz do projeto:

```sh
pytest
```
  1. Escolha um nome de usuário (para fins de demonstração, serve apenas para separar as notas de cada usuário)
  2. Crie uma nova nota
  3. Edite ou exclua suas notas criadas
