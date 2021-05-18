from database import execute
from database import print_results
from etl import CommandLine
from etl import Etl

USER_EVENTS_TABLE = "user_event"
USER_TABLE = "app_user"


class UsersEtl(Etl):
    table = USER_TABLE
    date_column = "start_date"

    def if_exists(self):
        query = f"""
            SELECT COUNT(*) AS cnt
            FROM {self.table}
            WHERE {self.date_column} = '{self.date}'
        """
        result = execute(query).first()[0]
        print(f"Count is {result}")
        return result

    def execute(self):
        if self.if_exists():
            print(
                f"There are records for {self.date}, therefore deleting them before insert"
            )
            execute(f"DELETE FROM {USER_EVENTS_TABLE} WHERE date = '{self.date}'")

        query = f"""
        INSERT INTO {self.table}
        SELECT
            id,
            event_type AS status,
            username AS name,
            user_email AS email,
            user_type AS type,
            organization_name,
            plan_name,
            received_at,
            date AS start_date
        FROM {USER_EVENTS_TABLE}
        WHERE date = '{self.date}'
        RETURNING *;
        """
        results = execute(query)
        print_results(results)


class UsersCli(CommandLine):
    etl_class = UsersEtl


if __name__ == "__main__":
    UsersCli().command()
