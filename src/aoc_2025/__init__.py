from importlib.metadata import version as get_version

__version__ = get_version(__package__)

def main() -> None:
    print("Hello from aoc-2025!")
