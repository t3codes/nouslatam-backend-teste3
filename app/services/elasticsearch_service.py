from elasticsearch import Elasticsearch
from typing import List, Dict
import os

ES_HOST = os.getenv("ELASTICSEARCH_HOST", "localhost")
ES_PORT = os.getenv("ELASTICSEARCH_PORT", 9200)

es = Elasticsearch([f"http://{ES_HOST}:{ES_PORT}"])

class ElasticsearchService:
    @staticmethod
    def is_connected() -> bool:
        return es.ping()

    @staticmethod
    def create_index_if_not_exists():
        if not es.indices.exists(index="posts"):
            es.indices.create(
                index="posts",
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
            print("Índice 'posts' criado no Elasticsearch!")

    @staticmethod
    def index_post(post_id: int, post_data: Dict) -> Dict:
        response = es.index(index="posts", id=post_id, document=post_data)
        return response

    @staticmethod
    def search_posts(field: str, query: str) -> List[Dict]:
        """
        Realiza uma pesquisa em um campo específico no Elasticsearch.
        
        :param field: O campo onde a pesquisa será realizada (ex: 'title', 'author', etc.)
        :param query: O termo de pesquisa.
        :return: Lista de posts que correspondem à pesquisa.
        """
        valid_fields = ["title", "author", "url", "score", "created_utc"]
        if field not in valid_fields:
            raise ValueError(f"Campo '{field}' não é válido. Escolha um dos seguintes campos: {', '.join(valid_fields)}")
        
        response = es.search(
            index="posts",  
            body={
                "query": {
                    "match": { 
                        field: query  
                    }
                }
            }
        )
        return [hit["_source"] for hit in response["hits"]["hits"]]
