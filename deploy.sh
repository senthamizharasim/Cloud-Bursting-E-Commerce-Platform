#!/bin/bash

SERVICE=$1
VERSION=$2

if [ -z "$SERVICE" ] || [ -z "$VERSION" ]; then
  echo "Usage: ./deploy.sh <service-name> <version>"
  echo "Example: ./deploy.sh order v7"
  exit 1
fi

echo "🚀 Building byteburst-$SERVICE:$VERSION..."
cd ~/Byteburst/$SERVICE-service
docker build -t byteburst-$SERVICE:$VERSION .

echo "📦 Loading image into Minikube..."
minikube image load byteburst-$SERVICE:$VERSION

echo "📝 Updating Kubernetes YAML..."
sed -i "s/image: byteburst-$SERVICE:.*/image: byteburst-$SERVICE:$VERSION/g" ~/Byteburst/k8s/$SERVICE.yaml

echo "🔄 Deploying and restarting pod..."
kubectl apply -f ~/Byteburst/k8s/$SERVICE.yaml
kubectl delete pod -l app=$SERVICE

echo "✅ Done! Wait a few seconds then run your port-forward command."