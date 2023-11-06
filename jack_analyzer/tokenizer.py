"""
Module with helper functions to parse and tokenize a .jack file

Should ignore newlines, spaces, and comments and then parse the remaining
pieces of a file into valid Jack tokens
"""
from __future__ import annotations
from collections import deque


def read_file(filename: str) -> list[str]:
    """Read a .jack file, and return it as a list of strings

    Args:
        `filename` (str): The absolute path to the file to be read

    Returns:
        `list[str]`: The file contents
    """

    with open(filename, "r", encoding="UTF-8") as f:
        contents = [line.strip() for line in f.readlines() if line not in ("\n", "")]
        return contents


def is_comment(line: str) -> bool:
    """Return true if provided line is a .jack comment.

    Single-line are signifed by `//`.  Multi-line comments by `/* */` or `/** */`
    and will likely be parsed differently

    Args:
        `line` (str): The unparsed .jack code line

    Returns:
        `bool`: If the line is a comment or not
    """
    return line.startswith("//")


def parse_file(filename: str) -> deque:
    """Read a .jack file line by line, parsing as necessary and adding to a `deque`

    Args:
        `filename` (str): A file to read

    Returns:
        `deque`: A deque (to be used as a stack) representing the tokenized file
    """
    raise NotImplementedError
