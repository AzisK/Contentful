import datetime
import json

from database import execute
from database import print_results
from etl import CommandLine
from etl import Etl


USER_EVENTS_JSON = "user_events.json"
USER_EVENTS_TABLE = "user_event"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


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
        insert_records = [str(t) for t in tuples]
        query = f"""
        INSERT INTO {self.table}
            (id, event_type, username, user_email, user_type, organization_name, plan_name, received_at, date)
            VALUES
            {",".join(insert_records)}
        RETURNING *;
        """
        results = execute(query)
        print_results(results)

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
                record["plan_name"] or "NULL",
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
