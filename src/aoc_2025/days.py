"""The code for each days challenge."""

from dataclasses import dataclass

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
