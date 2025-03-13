
Estudos dev - db - k8s 

Objetivo
O objetivo deste projeto é automatizar o processo de criação de infraestrutura e deploy de uma aplicação contendo Frontend, Backend e um banco de dados PostgreSQL no Kubernetes, utilizando apenas um script localizado dentro da Pasta 'infra' no repositório. 

Estrutura do Repositório
estudo_dev/
│
├── Backend/
│   ├── Docker/
│   │   └── api/
│   │       └── Dockerfile.api
│   ├── kube/
│   ├── backend_service.py
│
├── Frontend/
│   ├── Docker/
│   │   └── api/
│   │       └── Dockerfile.api
│   ├── kube/
│   ├── templates/
│   │   └── index.html
│   ├── frontend_service.py
│
├── infra/
│   ├── Logs-imagens/
│   │   └── logs
│   │   └── imagens
│   └── Start.sh
│
└── README.md



Pré-requisitos para execução. 
Antes de executar o script infra/Start.sh,  certifique-se de que você possui os seguintes pré-requisitos:

- Docker instalado e configurado no seu ambiente.
- Kubernetes e kubectl configurados e conectados ao seu cluster.
- Um repositório Docker configurado para enviar as imagens (ex: DockerHub).
- Estou aplicando em um pequeno Cluster testes EKS de estudo que possuo com suporte a EBS para persistência de dados, caso esteja usando minikube ou outro provider, alterar as configurações de storageclass e demais de acordo com a necessidade.


Etapas do script: 
1 - Criação do namespace Kubernetes.
2 - Aplicação dos arquivos de configuração do PostgreSQL no Kubernetes. 
3 - Criação das imagens Docker para o Backend e Frontend.
4 - Push das imagens Docker para o repositório.
5 - Aplicação dos arquivos Kubernetes do Backend e Frontend no Kubernetes.



Como Usar

Basta navegar até a pasta infra e executar o arquivo Start.sh em um bash de sua preferencia. 

$ sh Start.sh


O que o script faz:

Criação do Namespace Kubernetes: Se o namespace wa já existir, o script apenas avisa e segue para os próximos passos.

Aplicação dos arquivos de configuração do PostgreSQL: O script aplica arquivos YAML que configuram o ConfigMap, Secret, PersistentVolumeClaim, StatefulSet e Service para o banco de dados PostgreSQL no Kubernetes.

Criação das imagens Docker: O script cria imagens Docker para o Backend e Frontend e as envia para o repositório Docker.

Deploy do Backend e Frontend: Após a criação das imagens Docker, o script aplica os arquivos Kubernetes do Backend e Frontend no namespace wa.


Detalhamento do Processo

1. Criando o Namespace Kubernetes
O script verifica se o namespace wa já existe e, se não, o cria.

$kubectl create namespace wa


2. Aplicando os Arquivos de Configuração do PostgreSQL
Para garantir que o PostgreSQL seja configurado corretamente no Kubernetes, o script aplica os arquivos YAML sequencialmente:

$ kubectl apply -f ../db/kube/postgres-configmap.yaml -n wa
$ kubectl apply -f ../db/kube/postgres-secrets.yaml -n wa
$ kubectl apply -f ../db/kube/postgres-pvc.yaml -n wa
$ kubectl apply -f ../db/kube/postgres-statefulset.yaml -n wa
$ kubectl apply -f ../db/kube/postgres-services.yaml -n wa


3. Criando as Imagens Docker
O script cria imagens Docker para o Backend e Frontend usando os arquivos Dockerfile.api e depois as envia para o repositório Docker:

$ docker build -t tizil1987/backend:latest -f Docker/api/Dockerfile.api .
$ docker push tizil1987/backend:latest

$ docker build -t tizil1987/frontend:latest -f Docker/api/Dockerfile.api .
$ docker push tizil1987/frontend:latest


4. Aplicando os Arquivos Kubernetes do Backend e Frontend
O script aplica todos os arquivos de configuração Kubernetes para o Backend e Frontend:

$ kubectl apply -f ../Backend/kube/ -n wa
$ kubectl apply -f ../Frontend/kube/ -n wa


Exemplo de logs de Execução
Durante a execução do script, você verá saídas semelhantes a estas:

Error from server (AlreadyExists): namespaces "wa" already exists
configmap/postgres-config created
secret/postgres-secret created
persistentvolumeclaim/postgres-pvc created
statefulset.apps/postgres created
service/postgres created
[+] Building 1.5s (10/10) FINISHED
...
Essas saídas indicam que os recursos Kubernetes foram criados com sucesso e as imagens Docker foram enviadas para o repositório.



Considerações Finais
Cuidado com a criação do banco de dados: Ao rodar o script, se os volumes persistentes do PostgreSQL já existirem, eles serão reutilizados, caso contrário, novos volumes serão criados.
Modificação de Configurações: Se precisar alterar qualquer configuração (por exemplo, a quantidade de armazenamento para o PostgreSQL), edite os arquivos YAML no diretório db/kube/.
Verificação de Status: Após executar o script, é recomendável verificar o status dos pods e serviços Kubernetes:

$ kubectl get pods -n wa
$ kubectl get svc -n wa
