
# O Que Eu Faria Com Mais Tempo

Com mais tempo para trabalhar no projeto, eu faria as seguintes melhorias e implementações:

### 1. **Configuração de Credenciais no Elasticsearch e Kibana**

-   Configuraria autenticação e credenciais de segurança adequadas tanto no **Elasticsearch** quanto no **Kibana** para garantir um acesso seguro e controle de permissões. Isso incluiria o uso de usuários com diferentes níveis de permissão e a configuração de roles adequadas para restringir o acesso conforme necessário.
    

### 2. **Testes Abrangentes em Módulos Sensíveis**

-   Implementaria testes mais robustos, especialmente em módulos críticos como a **conexão entre containers** e os **serviços de consulta e post de dados no gerenciador de logs**. Isso garantiria que todos os componentes do sistema estivessem funcionando corretamente e que o sistema fosse resiliente a falhas.
    

### 3. **Aperfeiçoamento da Estrutura do Projeto**

-   A estrutura atual do projeto é bastante completa e abrange muitos dos meus conhecimentos nas stacks exploradas, como **FastAPI**, **Docker**, **PostgreSQL**, **Redis**, e **Elasticsearch**. No entanto, com mais tempo, faria um estudo mais profundo sobre o caso de uso e as **necessidades específicas de produção**, com o objetivo de otimizar o código e tornar a arquitetura ainda mais escalável e eficiente.
    

### 4. **Implantação de Serviços Sensíveis no Kubernetes**

-   Considerando a natureza sensível dos serviços, como a **API** que consulta o **Reddit**, migraria a aplicação para um **ambiente Kubernetes** para garantir melhor escalabilidade, alta disponibilidade e fácil gerenciamento de containers. Para otimizar o uso da API do Reddit, implementaria uma **segunda credencial de acesso** para balancear as requisições, permitindo que o sistema faça mais consultas sem sofrer bloqueios por **excesso de requests**.
- 
### 5.  **Notificação e Auto-Start para Sistemas Fora do Kubernetes**  

Para serviços que não estão dentro de um cluster Kubernetes, configuraria notificações de falha para monitorar qualquer parada inesperada desses sistemas. Essa configuração permitiria o estudo e a criação de pipelines de auto-start, onde, em caso de falhas, os sistemas seriam reiniciados automaticamente ou poderiam ser investigados e corrigidos rapidamente, minimizando o downtime e garantindo maior disponibilidade do sistema.
    

Além disso, colocaria alguns dos serviços, como **FastApi**, dentro de um cluster Kubernetes para aproveitar a escalabilidade e a gestão centralizada de recursos, garantindo maior resiliência e confiabilidade na infraestrutura.