CLIENT_CONTAINER = client
SERVER_CONTAINER = server

# Build and start the containers
build:
	docker-compose up --build -d

# Stop and remove containers
down:
	docker-compose down

# Stop containers and remove volumes
clean:
	docker-compose down -v

# Rebuild and restart containers
restart:
	docker-compose down && docker-compose up --build -d

# Show the current status of all containers
status:
	docker-compose ps

# Open a bash shell inside the client container
client-bash:
	docker-compose exec $(CLIENT_CONTAINER) bash

# Open a bash shell inside the server container
server-bash:
	docker-compose exec $(SERVER_CONTAINER) bash