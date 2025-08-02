import os
import requests
from elasticsearch import Elasticsearch

ES_HOST = os.getenv("ELASTICSEARCH_HOST", "localhost")
ES_PORT = os.getenv("ELASTICSEARCH_PORT", 9200)
KIBANA_HOST = os.getenv("KIBANA_HOST", "localhost")
KIBANA_PORT = os.getenv("KIBANA_PORT", 5601)

KIBANA_URL = f"http://{KIBANA_HOST}:{KIBANA_PORT}"
ELASTICSEARCH_URL = f"http://{ES_HOST}:{ES_PORT}"
ELASTICSEARCH_INDEX_POSTS = os.getenv("ELASTICSEARCH_INDEX_POSTS", "posts")
ELASTICSEARCH_INDEX_LOGS = os.getenv("ELASTICSEARCH_INDEX_LOGS", "logs_sistema")

def create_index_pattern(index_name: str):
    
    index_pattern_url = f"{KIBANA_URL}/api/saved_objects/index-pattern/{index_name}"
    body = {
        "attributes": {
            "title": index_name,  
            # "timeFieldName": "timestamp" 
        }
    }
    
    headers = {
        "kbn-xsrf": "true",
        "Content-Type": "application/json"
    }
    response = requests.post(index_pattern_url, json=body, headers=headers, auth=("elastic", "changeme"))
    
    if response.status_code == 200:
        print(f"Index Pattern '{index_name}' criado no Kibana!")
    else:
        print(f"Erro ao criar o Index Pattern: {response.status_code} - {response.text}")

def create_index_if_not_exists():
    es = Elasticsearch([f"http://{ES_HOST}:{ES_PORT}"])

    if not es.indices.exists(index=ELASTICSEARCH_INDEX_POSTS):
        es.indices.create(
            index=ELASTICSEARCH_INDEX_POSTS,
            body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                },
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "author": {"type": "text"},
                        "url": {"type": "text"},
                        "created_utc": {"type": "date"},
                        "score": {"type": "integer"}
                    }
                }
            }
        )
        print(f"Índice {ELASTICSEARCH_INDEX_POSTS} criado no Elasticsearch!")
        create_index_pattern(str(ELASTICSEARCH_INDEX_POSTS))

    if not es.indices.exists(index=ELASTICSEARCH_INDEX_LOGS):
        es.indices.create(
            index=ELASTICSEARCH_INDEX_LOGS,
            body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                },
                "mappings": {
                    "properties": {
                        "timestamp": {
                            "type": "date",
                            "format": "strict_date_time"  
                        },
                        "log_level": {"type": "keyword"},
                        "message": {"type": "text"},
                        "service": {"type": "keyword"},
                        "hostname": {"type": "keyword"}
                    }
                }
            }
        )
        print(f"Índice {ELASTICSEARCH_INDEX_LOGS} criado no Elasticsearch!")
        create_index_pattern(str(ELASTICSEARCH_INDEX_LOGS))


create_index_if_not_exists()
