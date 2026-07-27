"""An ABC for standardising a `days` code."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

STATIC = Path.cwd() / "static"


@dataclass
class Day(ABC):
    """Interface for a day's challenge from AOC 2025."""

    @abstractmethod
    def a(self) -> str: ...

    """Code for part a."""

    @abstractmethod
    def b(self) -> str: ...

    """Code for part b."""

    def run(self) -> tuple[str, str]:
        """Run the day's exercises.

        Returns:
            tuple[str, str]: respectively, the results of part A and B.
        """
        return (self.a(), self.b())
