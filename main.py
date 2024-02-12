"""
Python module for parsing [Polygon](https://polygon.codeforces.com) archive to Elan 
"""


def parse(elan_directory: str, polygon_archive_path: str, problem_id: int) -> None:
    directory = f"{elan_directory}/problems/problem{problem_id}/"