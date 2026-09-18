"""Utility functions for AOC."""

from typing import Generator


def count_surround(
    data: list[list[str]], val: str, threshold: int
) -> Generator[tuple[int, int], None, None]:
    """Determine if there are too many elements around a value.

    For a 2D grid, at each point, check how many of the surrounding points are ``val``.
    Then, check if that is < threshold.
    If less than threshould, return the coordinates.

    The can can be found by using the length.

    Args:
        data (list[list[str]]): a 2D data grid
        val (str): the check value
        threshold (int): how many cells is too many

    Returns:
        Generator[tuple[int, int], None, None]: generator of coordinates.
    """
    search = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if not (i == j == 0)]

    for x, row in enumerate(data):
        for y, cell in enumerate(row):
            if cell != val:
                continue
            count = [
                data[x + i][y + j] == val
                for i, j in search
                # boundary check
                if (0 <= x + i < len(data) and 0 <= y + j < len(row))
            ]
            if sum(count) < threshold:
                yield x, y
