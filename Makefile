build:
	docker build --no-cache --tag taejo_rest_api:0.1 .

start-taejo-api:
	docker run -d --gpus all --name taejo_rest_api -p 58032:8000 taejo_rest_api:0.1