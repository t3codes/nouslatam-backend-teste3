# log_handler.py
import logging
import socket
import datetime
import requests
import os

ES_HOST = os.getenv("ELASTICSEARCH_HOST") 
ES_PORT = os.getenv("ELASTICSEARCH_PORT")
ES_INDEX = os.getenv("ELASTICSEARCH_INDEX_LOGS", "logs_sistema")
SERVICE_NAME = os.getenv("SERVICE_NAME")

class ElasticsearchLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.hostname = socket.gethostname()
        self.url = f"http://{ES_HOST}:{ES_PORT}/{ES_INDEX}/_doc"

    def emit(self, record):
        try:
            log_entry = {
                "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "log_level": record.levelname,
                "message": self.format(record),
                "service": SERVICE_NAME,
                "hostname": self.hostname
            }   
            print("#"*40)
            print("#"*40)
            print(log_entry)
            print("#"*40)
            print("#"*40)
            headers = {"Content-Type": "application/json"}
            post_data = requests.post(self.url, json=log_entry, headers=headers, timeout=3)
            print(post_data.status_code)
            print(post_data.text)
        except Exception as e:
            print(f"[Logging error] Failed to send log to Elasticsearch: {e}")

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not any(isinstance(h, ElasticsearchLogHandler) for h in logger.handlers):
        es_handler = ElasticsearchLogHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        es_handler.setFormatter(formatter)
        logger.addHandler(es_handler)

    return logger
