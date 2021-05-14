# Dateengineering

## Setup

Make sure to have 
- Docker and Docker Compose installed
- Docker running

## Bring up the containers

`docker compose up`

## Refresh database

- `docker compose down`
- Check the volume name by `docker volume ls`
- `docker volume rm datengineering_database-data`
- `docker compose up`
