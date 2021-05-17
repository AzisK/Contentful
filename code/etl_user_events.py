import datetime
import json

from database import execute
from database import print_results
from etl import CommandLine
from etl import Etl

USER_EVENTS_JSON = "user_events.json"
USER_EVENTS_TABLE = "user_event"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
NEW_LINE = "\n"


def read_data():
    with open(USER_EVENTS_JSON) as file:
        data = json.load(file)
    return data


class UserEventsEtl(Etl):
    table = USER_EVENTS_TABLE

    def if_exists(self):
        query = f"""
            SELECT COUNT(*) AS cnt
            FROM {self.table}
            WHERE date = '{self.date}'
        """
        result = execute(query).first()[0]
        print(f"Count is {result}")
        return result

    def execute(self):
        data_today = self.get_today_data()

        if self.if_exists():
            print(
                f"There are records for {self.date}, therefore deleting them before insert"
            )
            execute(f"DELETE FROM {USER_EVENTS_TABLE} WHERE date = '{self.date}'")

        tuples = self.map_to_database(data_today)
        insert_records = self.tuples_to_str(tuples)
        query = f"""
        INSERT INTO {self.table}
            (id, event_type, username, user_email, user_type, organization_name, plan_name, received_at, date)
            VALUES
            {f",{NEW_LINE}".join(insert_records)}
        RETURNING *;
        """
        results = execute(query)
        print_results(results)

    def tuples_to_str(self, tuples):
        tuples_to_str = []
        for t in tuples:
            tuple_to_str = ",".join([f"'{f}'" if f else "NULL" for f in t])
            tuple_to_str = f"({tuple_to_str})"
            tuples_to_str.append(tuple_to_str)

        return tuples_to_str

    def get_today_data(self):
        data = read_data()
        data = self.add_date(data)
        data_today = [record for record in data if record["date"] == self.date]
        data_today = self.remove_duplicates(data_today)
        return data_today

    def remove_duplicates(self, dicts):
        return [dict(t) for t in {tuple(sorted(d.items())) for d in dicts}]

    def add_date(self, data):
        return [
            {
                **record,
                "date": str(
                    datetime.datetime.strptime(
                        record["received_at"], "%Y-%m-%d %H:%M:%S.%f"
                    ).date()
                ),
            }
            for record in data
        ]

    def map_to_database(self, records):
        tuples = [
            (
                record["id"],
                record["event_type"],
                record["username"],
                record["user_email"],
                record["user_type"],
                record["organization_name"],
                record["plan_name"],
                record["received_at"],
                record["date"],
            )
            for record in records
        ]
        return tuples


class UserEventsCli(CommandLine):
    etl_class = UserEventsEtl


if __name__ == "__main__":
    UserEventsCli().command()
