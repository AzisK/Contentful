import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv("database.env")

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = "db"
DB_PORT = "5432"


DB_STRING = "postgresql://{}:{}@{}:{}/{}".format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
)
DB = create_engine(DB_STRING)


def execute(query):
    with DB.connect() as connection:
        print(f"Executing\n{query}")
        return connection.execute(query)


def print_results(results):
    for r in results:
        print(r)
