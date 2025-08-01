
# **API de Trending Topics**

Este projeto é uma **API FastAPI** para consulta de tópicos populares. Ele utiliza **Docker** para orquestrar os serviços e tem integração com **PostgreSQL**, **Redis** e **Elasticsearch**.

## 📦 **Pré-requisitos**

Antes de rodar o projeto, você precisa ter o **Docker** instalado na sua máquina.

### 💡 **Instalação do Docker**:

- Para **Windows** ou **Mac**, siga o guia oficial: [Instalar Docker Desktop](https://www.docker.com/products/docker-desktop)
- Para **Linux**, siga o guia aqui: [Instalar Docker no Linux](https://docs.docker.com/engine/install/)

---

## 🚀 **Iniciar o Serviço**

### 1. Clone o repositório e acesse o direório:
```bash
git clone https://github.com/t3codes/nouslatam-backend-teste3.git
cd nouslatam-backend-teste3
```
### 2. Suba os containers Docker:
```bash
docker-compose up --build
```
Este comando vai:
Construir a imagem do FastAPI e levantar os containers para PostgreSQL, Redis e Elasticsearch.
O FastAPI estará disponível em: http://localhost:8000

### 3. Acesse a documentação da API:
Depois que o serviço estiver rodando, você pode acessar a documentação interativa do Swagger:
http://localhost:8000/docs
Acesse a Action no GitHub para verificar a execução da pipeline de CI: GitHub Actions

### 4. Informações Importantes
FastAPI: Framework usado para construir a API.
Docker: Utilizado para orquestrar os serviços.
PostgreSQL, Redis e Elasticsearch são serviços de banco de dados utilizados para o projeto.

### 5. O QUE EU FARIA COM MAIS TEMPO
...