from enum import Enum
import json
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv("database.env")

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = "db"
DB_PORT = "5432"
INITIAL_ORGANIZATIONS_JSON = "initial_organizations.json"
ORGANIZATIONS_TABLE = "organization"
TABLE_STATUS_TABLE = "init_table_by_python"

DB_STRING = "postgresql://{}:{}@{}:{}/{}".format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
)
DB = create_engine(DB_STRING)


class TABLE_STATUS(Enum):
    A = "Not Initialized"
    B = "Running"
    C = "Initialized"


def init():
    if get_table_status() == TABLE_STATUS.C.value:
        print("Therefore, the tables initialization by Python is skipped")
        return

    set_table_status(TABLE_STATUS.B.value)
    init_tables()
    set_table_status(TABLE_STATUS.C.value)


def get_table_status():
    is_table_result = execute(
        f"SELECT table_status FROM {TABLE_STATUS_TABLE} WHERE table_name = '{ORGANIZATIONS_TABLE}'"
    )
    first_row_status = is_table_result.first()[0]
    print(f'Table {ORGANIZATIONS_TABLE} is "{first_row_status}"')
    return first_row_status


def set_table_status(status):
    execute(
        f"""
        UPDATE {TABLE_STATUS_TABLE}
        SET table_status = '{status}'
        WHERE table_name = '{ORGANIZATIONS_TABLE}'
    """
    )


def init_tables():
    tuples = get_initial_data()

    insert_records = [str(t) for t in tuples]

    query = f"""
        INSERT INTO {ORGANIZATIONS_TABLE}
            (id, name, created) VALUES
            {",".join(insert_records)}
        ON CONFLICT (id) DO UPDATE
            SET name = excluded.name,
            created = excluded.created
        RETURNING *;
    """

    results = execute(query)
    print_results(results)


def execute(query):
    with DB.connect() as connection:
        print(f"Executing\n{query}")
        return connection.execute(query)


def get_initial_data():
    jsons = read_data()
    tuples = [
        (record["organization_key"], record["organization_name"], record["created_at"])
        for record in jsons
    ]
    return tuples


def read_data():
    with open(INITIAL_ORGANIZATIONS_JSON) as file:
        data = json.load(file)
    return data


def print_results(results):
    for r in results:
        print(r)


if __name__ == "__main__":
    print("Python tables initialization application started!")

    init()
