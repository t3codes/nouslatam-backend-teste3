
# **Gua de acesso e visualização de dados no Kibana**

Este documento irá explicar como acessar o Kibana e visualizar os logs no Elasticsearch.

### 1. Acessar Kibana

Kibana está sendo executado no Docker e pode ser acessado pelo navegador no seguinte endereço:

[http://localhost:5601](http://localhost:5601)

### 2. Visualizar Logs

Uma vez dentro do Kibana, siga as etapas para visualizar os logs:

1.  Na barra lateral esquerda, clique em **Discover**.
    
2.  No campo de seleção de índice, escolha o índice **logs_sistema** (ou o índice que você configurou para logs no seu ambiente).
    
3.  Agora você pode visualizar os logs gerados pela aplicação.
    

### 3. Configuração do Índice (caso necessário)

Os indices ou keys de serviço de logs são configurados automaticamente no build, mas se o índice `logs_sistema`  e `posts` não aparecer automaticamente, você pode configurar um padrão de índice em Kibana:

1.  Vá até **Management** > **Index Patterns**.
    
2.  Clique em **Create index pattern**.
    
3.  Digite `logs_sistema*` no campo de nome do índice, faça o mesmo com `posts` 
    
4.  Configure o campo de timestamp para a visualização de logs corretamente. OBS: apenas no logs_sistema pois la estao disponiveis os dados de timestamp.