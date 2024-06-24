#!/bin/bash

# Help
help() {
	echo "Usage: $0 [OPTIONS]"
	echo "Options:"
	echo "  -d  Deploy dev to cloud"
	echo "  -p  Deploy prod to cloud"
	echo "  -l  Deploy locally with docker-compose"
	echo "  -h  Show help"
}

# Build docker container and run it
while getopts dplh option; do
	case "${option}" in
	d) dev=true ;;
	p) prod=true ;;
	l) local=true ;;
	h)
		help
		exit
		;;
	esac
done

# If no options show help
if [ $# -eq 0 ]; then
	help
	exit
fi

if [ "$dev" = true ]; then
	echo "Deploying dev to cloud..."
	gcloud builds submit --config=deploy/dev/cloudbuild.yaml
fi

if [ "$prod" = true ]; then
	echo "Deploying prod to cloud..."
	echo "Deploying extract-service..."
	gcloud builds submit --config=deploy/prod/cloudbuild_extract.yaml
	echo "Deploying transform-service..."
	gcloud builds submit --config=deploy/prod/cloudbuild_transform.yaml
	echo "Deploying load-service..."
	gcloud builds submit --config=deploy/prod/cloudbuild_load.yaml
fi

if [ "$local" = true ]; then
	echo "Deploying locally with docker-compose..."
	docker-compose up -d
fi
