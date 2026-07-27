"""AOC 2025 code."""

from argparse import ArgumentParser
from inspect import getmembers, isclass

import aoc_2025.days as days


def main() -> None:
    """Entrypoint for CLI."""
    classes = {
        name.lower(): member
        for (name, member) in getmembers(
            days, lambda c: isclass(c) and c.__module__ == days.__name__
        )
    }

    parser = ArgumentParser(description="Advent of Code, 2025", suggest_on_error=True)
    parser.add_argument("day", type=str, help="Which day to run", choices=["one"])
    args = parser.parse_args()

    print(classes[args.day]().run())
