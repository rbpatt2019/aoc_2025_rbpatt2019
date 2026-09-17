"""The code for each days challenge."""

import re
from dataclasses import dataclass
from itertools import combinations

from .base_class import STATIC, Day


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
