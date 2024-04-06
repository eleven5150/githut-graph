import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from argparse import Namespace


@dataclass
class Stat:
    year: int
    quarter: int
    count: int


def parse_args() -> Namespace:
    parser = argparse.ArgumentParser(description="Tool for drawing graphs based on data from githut")
    parser.add_argument("-i", "--input_path",
                        type=Path,
                        required=True,
                        help="Path input json file")
    parser.add_argument("-l", "--languages",
                        nargs="+",
                        required=True,
                        help="List of languages to draw on graph")
    return parser.parse_args()


def main() -> None:
    args: Namespace = parse_args()
    with open(args.input_path, "rt") as input_file:
        input_data: str = input_file.read()

    data = json.loads(input_data)

    stats: dict[str, list[Stat]] = dict()
    for language in args.languages:
        stats.update({language: list()})

    for item in data:
        if item["name"] in args.languages:
            stats[item["name"]].append(Stat(
                item["year"],
                item["quarter"],
                item["count"]
            ))

    print("")


if __name__ == '__main__':
    main()
