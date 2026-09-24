"""The code for each days challenge."""

import math
import re
from dataclasses import dataclass
from itertools import combinations, groupby

from .base_class import STATIC, Day
from .utils import count_surround


@dataclass
class One(Day):
    """Day one."""

    length: int = 100
    start: int = 50
    marker: int = 0

    def a(self) -> str:
        """Calculate the number of times the dial is set to marker.

        We can use modulo division to account for rollover on either end of the list.

        Returns:
            str: the number of times the dial is set to marker.
        """
        with open(STATIC / "1a.txt") as file:
            moves = [
                int(line.strip().replace("R", "").replace("L", "-")) for line in file
            ]
            idx = self.start
            count = 0

            for move in moves:
                idx = (idx + move) % self.length
                count += idx == self.marker

        return str(count)

    def b(self) -> str:
        """Calculate the number of times the dial is set OR passes marker.

        Turns out, the most straightforward way to do this is simply to create a list of crossed values
               and then count the number of 0s.

        Returns:
                   str: the number of times the dial is set to marker.
        """
        with open(STATIC / "1a.txt") as file:
            moves = [
                int(line.strip().replace("R", "").replace("L", "-")) for line in file
            ]
            print(max(moves), min(moves))
            idx = self.start
            count = 0

            for move in moves:
                crossed_vals = [
                    x % self.length
                    for x in range(idx, idx + move, -1 if move < 0 else 1)
                ]
                count += sum([x == self.marker for x in crossed_vals])
                idx = (idx + move) % self.length

        return str(count)


@dataclass
class Two(Day):
    """Day two."""

    def a(self) -> str:
        """Find all numbers in a range that have symmetrical halves.

        Returns:
            str: the sum of all numbers that are symmetrical.
        """
        with open(STATIC / "2a.txt") as file:
            ranges = [pair.split("-") for pair in file.readline().strip().split(",")]
            ranges = [range(int(x), int(y) + 1) for (x, y) in ranges]

        def _is_symmetric(x: int) -> bool:
            """Test if an integer is symmetric."""
            val = str(x)
            length = len(val)
            if length % 2 == 0:
                return val[: length // 2] == val[length // 2 :]
            return False

        return str(sum(x for span in ranges for x in span if _is_symmetric(x)))

    def b(self) -> str:
        r"""Find all numbers that are composed of substrings.

        I initially thought to generalise the above to accept a substring parameter,
        rather than just hardcoding 2;
        however, it creates an ugly loop to check over all those values for each entry in the range.
        Regex provides a tidy solution!
        Explanation: ``(.+)`` capture a group composed of any number of any characters
        ``\1+`` match the group any number of times

        We then use full match to make sure that the whole string is a match,
        avoiding matches in strings like ``1232323234``.

        Returns:
            str: the sum of all numbers that are composed of substrings.
        """
        with open(STATIC / "2a.txt") as file:
            ranges = [pair.split("-") for pair in file.readline().strip().split(",")]
            ranges = [range(int(x), int(y) + 1) for (x, y) in ranges]

        pattern = re.compile(r"(.+)\1+")
        return str(sum(x for span in ranges for x in span if pattern.fullmatch(str(x))))


@dataclass
class Three(Day):
    """Day three."""

    def a(self) -> str:
        """Find the largest pair of numbers in a string.

        Returns:
            str: The sum of all maximum pairs.
        """
        with open(STATIC / "3.txt") as file:
            batteries = [line.strip() for line in file]

        return str(
            sum(
                int("".join(sorted(combinations(bank, 2), reverse=True)[0]))
                for bank in batteries
            )
        )

    def b(self) -> str:
        """So the above absolutely fried my Mac when looking for 12-ples.

        Instead, we need to implement a more efficient search.
        Thank you to many google hits for help.

        Returns:
            str: The sum of all maximum 12-ples.
        """
        with open(STATIC / "3.txt") as file:
            batteries = [line.strip() for line in file]

        def _max(bank: str, size: int) -> int:
            """Find the largest size-tuple in a string."""
            val = ""
            split = list(bank)
            while size > 0:
                size -= 1
                max_val = max(split[: len(split) - size])
                val += max_val
                split = split[split.index(max_val) + 1 :]
            return int(val)

        return str(sum(_max(bank, 12) for bank in batteries))


@dataclass
class Four(Day):
    """Day four."""

    def a(self) -> str:
        """Find the number of @ signs around a point.

        Returns:
            str: The number of rolls with 4 or less surrounding.
        """
        with open(STATIC / "4.txt") as file:
            grid = [list(line.strip()) for line in file.readlines()]
        return str(len(list(count_surround(grid, "@", 4))))

    def b(self) -> str:
        """Find total number of rolls.

        It's unclear to me from the prompt whether this is a greedy search or an optimised solution.
        Choosing to be greedy. Just keep running until length is 0.

        Returns:
            str: The number of rolls that can be removed.
        """
        with open(STATIC / "4.txt") as file:
            grid = [list(line.strip()) for line in file.readlines()]

        count = 0
        while len(rolls := list(count_surround(grid, "@", 4))) > 0:
            count += len(rolls)
            for x, y in rolls:
                grid[x][y] = "."
        return str(count)


@dataclass
class Five(Day):
    """Day five.

    I got thoroughly nerd sniped and tried to implement a search for the first.
    Turns out, relatively straightforward list comprehensions will solve both parts.
    """

    def a(self) -> str:
        """Figure out which values are in a range."""
        with open(STATIC / "5.txt") as file:
            contents = [line.strip() for line in file]

        split_idx = contents.index("")
        ranges = [[int(y) for y in x.split("-")] for x in contents[:split_idx]]
        vals = [int(x) for x in contents[split_idx + 1 :]]

        return str(
            len(
                [
                    val
                    for val in vals
                    if any(val >= left and val <= right for left, right in ranges)
                ]
            )
        )

    def b(self) -> str:
        """Figure out values in every range."""
        with open(STATIC / "5.txt") as file:
            contents = [line.strip() for line in file]

        split_idx = contents.index("")
        ranges = sorted([int(y) for y in x.split("-")] for x in contents[:split_idx])

        merged = [ranges[0]]
        for span in ranges[1:]:
            if merged[-1][0] <= span[0] <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], span[1])
            else:
                merged.append(span)
        return str(sum(right - left + 1 for left, right in merged))


@dataclass
class Six(Day):
    """Day six."""

    def a(self) -> str:
        """Perform column-wise operations, where the operator is in the last row."""
        with open(STATIC / "6.txt") as file:
            columns = list(zip(*[line.strip().split() for line in file], strict=True))

        total = 0
        for col in columns:
            match col[-1]:
                case "+":
                    total += sum(int(x) for x in col[:-1])
                case "*":
                    total += math.prod(int(x) for x in col[:-1])
                case _:
                    raise Exception("Operation not supported.")
        return str(total)

    def b(self) -> str:
        """Right to left, column-wise, white space significant parsing.

        Comments left in code for more details.
        """
        with open(STATIC / "6.txt") as file:
            *nums, ops = [line.strip("\n") for line in file]

        # Classic nested list rotation
        columns = list(zip(*nums, strict=True))[::-1]
        ops = ops.split()[::-1]

        # Use groupby to split on columns that are fully white space
        integers = [
            [int("".join(col)) for col in group]
            for key, group in groupby(
                columns, key=lambda col: all(char == " " for char in col)
            )
            if not key
        ]

        # Do the math
        total = 0
        for group, op in zip(integers, ops, strict=True):
            match op:
                case "+":
                    total += sum(int(x) for x in group)
                case "*":
                    total += math.prod(int(x) for x in group)
                case _:
                    raise Exception("Operation not supported.")

        return str(total)


@dataclass
class Seven(Day):
    """Day 7."""

    def a(self) -> str:
        """Find the number of beam splits in the input."""
        with open(STATIC / "7.txt") as file:
            header, *lines = [line.strip() for line in file]

        # Set a beam at the initial position
        beams = [False] * len(header)
        beams[header.index("S")] = True

        # Count splits, as multiple beams could end up in each slot
        splits = 0
        for line in lines:
            for i, char in enumerate(line):
                if char == "^" and beams[i]:
                    beams[i - 1] = True
                    beams[i + 1] = True
                    beams[i] = False
                    splits += 1

        return str(splits)

    def b(self) -> str:
        """Count the number of possible paths.

        The number of active timelines is the same as the sum of the number of paths that go through each column.
        We can achieve this by simply counting rather than storing booleans.
        """
        with open(STATIC / "7.txt") as file:
            header, *lines = [line.strip() for line in file]

        # Set a beam at the initial position
        beams = [0] * len(header)
        beams[header.index("S")] = 1

        for line in lines:
            for i, char in enumerate(line):
                if char == "^" and beams[i]:
                    beams[i - 1] += beams[i]
                    beams[i + 1] += beams[i]
                    beams[i] = 0

        return str(sum(beams))
