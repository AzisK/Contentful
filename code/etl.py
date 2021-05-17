import argparse
import datetime

DATE_FORMAT = "%Y-%m-%d"


def parse_args():
    parser = argparse.ArgumentParser(prog="ETL", description="CLI ETL tool")
    parser.add_argument("date", help="Date of the ETL run")
    args = parser.parse_args()
    return args


def validate_args(args):
    try:
        datetime.datetime.strptime(args.date, DATE_FORMAT)
    except ValueError:
        raise Exception("Date format is incorrect. It should be YYYY-MM-DD.")


class Etl:
    def __init__(self, args):
        self.date = args.date

    def execute(self):
        print(
            "Hi, 'execute' has not been specified, I am simply printing this message."
        )


class CommandLine:
    etl_class = Etl

    def __init__(self):
        args = parse_args()
        validate_args(args)
        self.etl = self.etl_class(args)

    def command(self):
        self.etl.execute()


if __name__ == "__main__":
    CommandLine().command()
