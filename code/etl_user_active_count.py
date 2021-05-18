from database import execute
from database import print_results
from etl import CommandLine
from etl import Etl

USER_EVENTS_TABLE = "user_event"
USER_ACTIVE_COUNT_TABLE = "user_active_count"


class UsersActiveCountEtl(Etl):
    table = USER_ACTIVE_COUNT_TABLE
    date_column = "start_date"

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
        if self.if_exists():
            print(
                f"There are records for {self.date}, therefore deleting them before insert"
            )
            execute(f"DELETE FROM {self.table} WHERE date = '{self.date}'")

        query = f"""
        INSERT INTO {self.table}
        SELECT
            '{self.date}' AS date,
            COUNT(t.*)
        FROM
            (SELECT DISTINCT ON (id)
                id,
                event_type AS status,
                username AS name,
                user_email AS email,
                user_type AS type,
                organization_name,
                plan_name,
                received_at,
                date
            FROM {USER_EVENTS_TABLE} t1
            WHERE
                date <= '{self.date}'
            ORDER BY id, received_at DESC
        ) t
        WHERE t.status <> 'User Deleted'
        RETURNING *
        """
        results = execute(query)
        print_results(results)


class UsersActiveCountCli(CommandLine):
    etl_class = UsersActiveCountEtl


if __name__ == "__main__":
    UsersActiveCountCli().command()
