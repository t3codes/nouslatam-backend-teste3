import pytest
import warnings
import os
from unittest.mock import patch, Mock
from elasticsearch import Elasticsearch, ElasticsearchWarning
from services.elasticsearch_initializer import create_index_if_not_exists, create_index_pattern, ELASTICSEARCH_INDEX_POSTS, ELASTICSEARCH_INDEX_LOGS, KIBANA_URL

# Fixture para o cliente Elasticsearch
@pytest.fixture
def elasticsearch_client():
    """Fixture para fornecer um cliente Elasticsearch."""
    warnings.filterwarnings("ignore", category=ElasticsearchWarning)
    
    # Usa as variáveis de ambiente do docker-compose
    es_host = os.getenv("ELASTICSEARCH_HOST", "elasticsearch")
    es_port = os.getenv("ELASTICSEARCH_PORT", "9200")
    client = Elasticsearch([f"http://{es_host}:{es_port}"])
    
    if not client.ping():
        pytest.skip(f"Elasticsearch não está disponível em http://{es_host}:{es_port}")
    
    # Usa índices de teste exclusivos
    test_index_posts = "test_posts"
    test_index_logs = "test_logs_sistema"
    
    # Limpa os índices de teste antes de cada teste
    if client.indices.exists(index=test_index_posts):
        client.indices.delete(index=test_index_posts)
    if client.indices.exists(index=test_index_logs):
        client.indices.delete(index=test_index_logs)
    
    # Log para verificar os valores antes do patch
    print(f"Valores originais - ELASTICSEARCH_INDEX_POSTS: {ELASTICSEARCH_INDEX_POSTS}, ELASTICSEARCH_INDEX_LOGS: {ELASTICSEARCH_INDEX_LOGS}")
    
    # Sobrescreve as variáveis de índice para os testes
    with patch("services.elasticsearch_initializer.ELASTICSEARCH_INDEX_POSTS", test_index_posts) as mock_posts:
        with patch("services.elasticsearch_initializer.ELASTICSEARCH_INDEX_LOGS", test_index_logs) as mock_logs:
            # Log para verificar os valores após o patch
            print(f"Valores após patch - ELASTICSEARCH_INDEX_POSTS: {ELASTICSEARCH_INDEX_POSTS}, ELASTICSEARCH_INDEX_LOGS: {ELASTICSEARCH_INDEX_LOGS}")
            yield client
    
    # Limpa os índices de teste após o teste
    if client.indices.exists(index=test_index_posts):
        client.indices.delete(index=test_index_posts)
    if client.indices.exists(index=test_index_logs):
        client.indices.delete(index=test_index_logs)

# Testes que dependem do Elasticsearch
class TestElasticsearchInitializer:
       

    def test_no_duplicate_index_creation(self, elasticsearch_client):
        """Testa que índices existentes não são recriados."""
        test_index_posts = "test_posts"
        test_index_logs = "test_logs_sistema"
        elasticsearch_client.indices.create(index=test_index_posts)
        elasticsearch_client.indices.create(index=test_index_logs)
        
        with patch("services.elasticsearch_initializer.create_index_pattern") as mock_create_index_pattern:
            create_index_if_not_exists()
            
            print(f"Chamadas a create_index_pattern: {mock_create_index_pattern.call_args_list}")
            mock_create_index_pattern.assert_not_called()

# Testes que não dependem do Elasticsearch
class TestKibanaInitializer:
    @patch("services.elasticsearch_initializer.requests.post")
    def test_create_index_pattern_success(self, mock_post):
        """Testa a criação de um padrão de índice no Kibana com resposta bem-sucedida."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Success"
        mock_post.return_value = mock_response
        
        create_index_pattern("test-index")
        
        mock_post.assert_called_once_with(
            f"{KIBANA_URL}/api/saved_objects/index-pattern/test-index",
            json={"attributes": {"title": "test-index"}},
            headers={"kbn-xsrf": "true", "Content-Type": "application/json"},
            auth=("elastic", "changeme")
        )

    @patch("services.elasticsearch_initializer.requests.post")
    def test_create_index_pattern_failure(self, mock_post):
        """Testa a criação de um padrão de índice no Kibana com falha."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response
        
        create_index_pattern("test-index")
        
        mock_post.assert_called_once_with(
            f"{KIBANA_URL}/api/saved_objects/index-pattern/test-index",
            json={"attributes": {"title": "test-index"}},
            headers={"kbn-xsrf": "true", "Content-Type": "application/json"},
            auth=("elastic", "changeme")
        )