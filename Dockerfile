FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
# Instalar dependências necessárias
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https 

COPY ./app /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
