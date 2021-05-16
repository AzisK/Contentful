import json

from etl import CommandLine
from etl import Etl

USER_EVENTS_JSON = "user_events.json"


def read_data():
    with open(USER_EVENTS_JSON) as file:
        data = json.load(file)
    return data


class UserEventsEtl(Etl):
    def execute(self):
        data = read_data()
        print(data)


class UserEventsCli(CommandLine):
    etl_class = UserEventsEtl


if __name__ == "__main__":
    UserEventsCli().command()
