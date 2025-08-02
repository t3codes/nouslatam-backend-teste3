from elasticsearch import Elasticsearch
import os
import time
import requests

ES_HOST = os.getenv("ELASTICSEARCH_HOST", "localhost")
ES_PORT = os.getenv("ELASTICSEARCH_PORT", 9200)
KIBANA_HOST = os.getenv("KIBANA_HOST", "localhost")
KIBANA_PORT = os.getenv("KIBANA_PORT", 5601)

ELASTICSEARCH_URL = f"http://{ES_HOST}:{ES_PORT}"
KIBANA_URL = f"http://{KIBANA_HOST}:{KIBANA_PORT}"

def wait_for_elasticsearch():
    print("Aguardando Elasticsearch...")
    es = Elasticsearch([ELASTICSEARCH_URL])
    for _ in range(30):  # Tenta por 30 segundos
        try:
            if es.ping():
                print("Elasticsearch está pronto!")
                return True
        except Exception:
            pass
        time.sleep(1)
    raise Exception("Elasticsearch não está disponível")

def wait_for_kibana():
    print("Aguardando Kibana...")
    for _ in range(30):  # Tenta por 60 segundos
        try:
            response = requests.get(f"{KIBANA_URL}/api/status")
            if response.status_code == 200:
                print("Kibana está pronto!")
                return True
        except Exception:
            pass
        time.sleep(1)
    raise Exception("Kibana não está disponível")

if __name__ == "__main__":
    wait_for_elasticsearch()
    wait_for_kibana()