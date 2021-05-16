# Datengineering

## Setup

Make sure to have
- Docker and Docker Compose installed
- Docker running

## Bring up the containers

`docker compose up`

## Connect to Python container

`docker exec -it datengineering_python_1 bash`

## Look at database via Adminer

`http://localhost:8080/?pgsql=db&username=user&db=db&ns=public`

## Refresh database

- `docker compose down`
- Check the volume name by `docker volume ls`
- `docker volume rm datengineering_database-data`
- `docker compose up`
