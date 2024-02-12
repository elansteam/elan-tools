from __future__ import annotations
from dataclasses import dataclass


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
    legend: str # path to legend.mdx
    name: str # path to name.mdx
    output: str # path to output.mdx
    tests: list[ElanProblemExampleTest]

@dataclass
class ElanProblemExampleTest:
    input: str
    output: str
