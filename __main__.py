import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from argparse import Namespace
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


def quarter_to_float(quarter: int) -> float:
    return (quarter - 1) * 0.25


@dataclass
class Stat:
    lang: str
    year: int
    quarter: int
    count: int


@dataclass
class Count:
    year: int
    quarter: int
    count: int


@dataclass
class LangData:
    stats: dict[str, list[Count]]
    sum_counts: dict[str, int]

    @classmethod
    def prepare_lang_data(cls, stats: list[Stat], languages: list[str]) -> "LangData":
        sum_counts: dict[str, int] = dict()
        lang_stats: dict[str, list[Count]] = dict()

        for language in languages:
            lang_stats.update({language: list()})

        curr_year: int = stats[0].year
        curr_quarter: int = stats[0].quarter
        count_sum: int = 0
        for item in stats:
            if item.year == curr_year and item.quarter == curr_quarter:
                count_sum += item.count
            else:
                sum_counts.update({f"{curr_year}.{curr_quarter}": count_sum})
                count_sum = 0
                curr_year: int = item.year
                curr_quarter: int = item.quarter

            if item.lang in languages:
                lang_stats[item.lang].append(
                    Count(
                        item.year,
                        item.quarter,
                        item.count
                    )
                )
        sum_counts.update({f"{curr_year}.{curr_quarter}": count_sum})

        return cls(
            stats=lang_stats,
            sum_counts=sum_counts
        )

    def plot_graph(self, width: int, height: int) -> None:

        for lang, counts in self.stats.items():
            years: list[float] = list()
            values: list[float] = list()
            for count in counts:
                years.append(count.year + quarter_to_float(count.quarter))

                sum_count: int = self.sum_counts[f"{count.year}.{count.quarter}"]
                values.append(count.count / sum_count)
            plt.plot(years, values, label=lang, linewidth=5.0)

        plt.yscale("log")
        leg = plt.legend(bbox_to_anchor=(0.96, 1.0), loc="upper left")
        for text in leg.get_texts():
            text.set_fontsize(20)

        plt.title("Количество репозиториев на GitHub, % от общего числа", fontsize=30)
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
        plt.grid()

        plt.gcf().set_size_inches(width, height)
        plt.savefig("graph.png", dpi=600)
        # plt.show()


def parse_args() -> Namespace:
    parser = argparse.ArgumentParser(description="Tool for drawing graphs based on data from githut")
    parser.add_argument("-i", "--input_path",
                        type=Path,
                        required=True,
                        help="Path input json file")
    parser.add_argument("-w", "--width",
                        type=int,
                        required=True,
                        help="Width of graph in inches")
    parser.add_argument("-t", "--tallness",
                        type=int,
                        required=True,
                        help="Height of graph in inches")
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

    stats: list[Stat] = list()

    for item in data:
        stats.append(
            Stat(
                item["name"],
                int(item["year"]),
                int(item["quarter"]),
                int(item["count"])
            )
        )

    lang_data: LangData = LangData.prepare_lang_data(stats, args.languages)

    lang_data.plot_graph(args.width, args.tallness)


if __name__ == '__main__':
    main()
