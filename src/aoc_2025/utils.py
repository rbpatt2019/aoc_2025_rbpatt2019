"""Utility functions for AOC."""

from typing import Generator, Iterable


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


class UnionFind[T]:
    """The Union-Find, or Disjoint Set, class.

    Attributes:
        parents (dict[T, T]): an elements parent.
        size (dict[T, int]): the size of each node.
    """

    def __init__(self, elements: Iterable[T]) -> None:
        """Create an instance of UnionFind.

        Args:
            elements (Iterable[T]): an iterable of any type
        """
        items = list(elements)
        self.parents = {i: i for i in items}
        self.size = dict.fromkeys(items, 1)

    @property
    def set_sizes(self) -> list[int]:
        """Integer sizes of all groups."""
        return list(self.size.values())

    def find(self, element: T) -> T:
        """Find the root of the tree that contains element.

        Use path compression to speed up calls.
        """
        if self.parents[element] != element:
            self.parents[element] = self.find(self.parents[element])
        return self.parents[element]

    def union(self, el1: T, el2: T) -> None:
        """Set one root as the parent of the other root.

        Use union by size to reduce tree height.
        This always uses the tree with more decendants as the parent.
        """
        root1, root2 = self.find(el1), self.find(el2)

        # Do  nothing if they are already in the same tree
        if root1 == root2:
            return

        # Ensure root1 is always the tree with more descendants
        if self.size[root1] < self.size[root2]:
            root1, root2 = root2, root1

        # Set parent and update size
        self.parents[root2] = root1
        self.size[root1] += self.size[root2]

        # root2 is no longer a root
        del self.size[root2]
