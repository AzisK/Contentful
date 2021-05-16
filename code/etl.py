import argparse


def parse_args():
    parser = argparse.ArgumentParser(prog="ETL", description="CLI ETL tool")
    parser.add_argument("date", help="Date of the ETL run")
    args = parser.parse_args()
    return args


def command_line():
    args = parse_args()
    print(args)


if __name__ == "__main__":
    command_line()
