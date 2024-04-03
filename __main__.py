import argparse
import sys
from pathlib import Path
from argparse import Namespace


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
    print(args.languages)


if __name__ == '__main__':
    main()
