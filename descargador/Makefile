# Configura tus variables aquí
IMAGE_NAME=descargador-audio-video
DOCKER_USER=moncholv
TAG=latest

# Construir la imagen
build:
	docker build -t $(IMAGE_NAME) .

# Etiquetar con Docker Hub
tag:
	docker tag $(IMAGE_NAME) $(DOCKER_USER)/$(IMAGE_NAME):$(TAG)

# Subir a Docker Hub
push:
	docker push $(DOCKER_USER)/$(IMAGE_NAME):$(TAG)

# Comando completo
publish: build tag push
