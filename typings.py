from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class ElanProblem:
    problem_id: int
    problem_short_name: str
    time_limit: int # milliseconds
    memory_limit: int # bytes
    variants: dict[str, ElanProblemLocalized]

@dataclass
class ElanProblemLocalized:
    problem_id: int
    problem_short_name: str
    name: str
    statements: ElanProblemStatements

@dataclass
class ElanProblemStatements:
    input: str # path to input.mdx
    output: str # path to output.mdx
    tests: list[ElanProblemExampleTest]
    name: str | None = None # path to name.mdx
    legend: str | None = None # path to legend.mdx
    scoring: str | None = None # path to scoring.mdx
    notes: str | None = None # path to notes.mdx
    tutorial: str | None = None # path to tutorial.mdx

@dataclass
class ElanProblemExampleTest:
    input: str
    output: str

class InvalidProblem(Exception):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return super().__call__(*args, **kwds)
