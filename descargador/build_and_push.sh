#!/bin/bash

# Configura tus variables
IMAGE_NAME=descargador-audio-video
DOCKER_USER=moncholv
TAG=latest

# Construir la imagen
echo "🛠️  Construyendo imagen Docker..."
docker build -t $IMAGE_NAME .

# Etiquetar para Docker Hub
echo "🏷️  Etiquetando como $DOCKER_USER/$IMAGE_NAME:$TAG"
docker tag $IMAGE_NAME $DOCKER_USER/$IMAGE_NAME:$TAG

# Subir a Docker Hub
echo "☁️  Subiendo imagen a Docker Hub..."
docker push $DOCKER_USER/$IMAGE_NAME:$TAG

echo "✅ Imagen publicada: https://hub.docker.com/r/$DOCKER_USER/$IMAGE_NAME"
