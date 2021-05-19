# Datengineering

## Setup

Make sure to have
- Docker and Docker Compose installed
- Docker running

## Bring up the containers

`docker compose up`

## Connect to Python container

`docker exec -it datengineering_python_1 bash`. Python code can be executed from inside Python container.

## ETLs in repository

Repo consists of 3 ETLs.
1. `etl_user_events.py` ETL should be loaded first since other calculations depend on it
2. `etl_users.py` can be loaded after 1
3. `etl_user_active_count` can be loaded after 1

## Run an ETL in Python container

At the moment there is data for dates from 2020-12-05 to 2020-12-11. Run an ETL for a day like this `python etl_user_events.py 2020-12-08`

## Run tests inside Python container

`python -m pytest`

## Look at database via Adminer

`http://localhost:8080/?pgsql=db&username=user&db=db&ns=public`

## Refresh database

- `docker compose down`
- Check the volume name by `docker volume ls`
- `docker volume rm datengineering_database-data`
- `docker compose up`
