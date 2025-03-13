#!/bin/bash

#Criando namespace - caso tenha o namespace criado vai te avisa e seguir o fluxo... 
kubectl create namespace wa 

sleep 3 

#Aplicando arquivos kubernetes Postgres no namespace 'wa' - poderia colocar a pasta, mas se ele não segue uma sequencia
# vai nos obrigar a agir manualmente... Por isso vou arquivo a arquivo... 
kubectl apply -f ../db/kube/postgres-configmap.yaml -n wa
sleep 3
kubectl apply -f ../db/kube/postgres-secrets.yaml -n wa
sleep 3
kubectl apply -f ../db/kube/postgres-pvc.yaml -n wa
sleep 3
kubectl apply -f ../db/kube/postgres-statefulset.yaml -n wa
sleep 3
kubectl apply -f ../db/kube/postgres-services.yaml -n wa

sleep 3

cd .. 

cd Backend

#Criando Imagem docker backend
docker build -t tizil1987/backend:latest -f Docker/api/Dockerfile.api .

#Subindo Imagem docker backend para repo 
docker push tizil1987/backend:latest

sleep 3

cd .. 

cd Frontend

#Criando Imagem docker frontend
docker build -t tizil1987/frontend:latest -f Docker/api/Dockerfile.api .

#Subindo Imagem docker frontend para repo 
docker push tizil1987/frontend:latest

sleep 10

#Aplicando todos os arquivos kubernetes Backend no namespace 'wa'
kubectl apply -f ../Backend/kube/ -n wa

sleep 10

#Aplicando todos os arquivos kubernetes Frontend no namespace 'wa'
kubectl apply -f ../Frontend/kube/ -n wa




