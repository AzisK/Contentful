import argparse


def parse_args():
    parser = argparse.ArgumentParser(prog="ETL", description="CLI ETL tool")
    parser.add_argument("date", help="Date of the ETL run")
    args = parser.parse_args()
    return args


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
        self.etl = self.etl_class(args)

    def command(self):
        self.etl.execute()


if __name__ == "__main__":
    CommandLine().command()
