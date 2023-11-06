"""
Module with helper functions to parse and tokenize a .jack file

Should ignore newlines, spaces, and comments and then parse the remaining
pieces of a file into valid Jack tokens
"""
from __future__ import annotations
from collections import deque

from constants import COMMENT, ML_COMMENT_START, ML_COMMENT_END


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


def is_single_comment(line: str) -> bool:
    """Return true if provided line is a .jack comment.

    Single-line are signifed by `//`.  Multi-line comments by `/* */` or `/** */`
    and are parsed differently because we can't necessarily just throw the whole line away

    Args:
        `line` (str): The unparsed .jack code line

    Returns:
        `bool`: If the line is a single-line comment or not
    """

    return line.startswith(COMMENT)


def is_full_ml_comment(line: str) -> bool:
    """Returns true if provided line is a .jack multi-line comment

    Args:
        `line` (str): The unparsed .jack code line

    Returns:
        `bool`: If the line is a multi-line comment or not
    """

    return line.startswith(ML_COMMENT_START) and line.endswith(ML_COMMENT_END)


def parse_file(filename: str) -> deque:
    """Read a .jack file line by line, parsing as necessary and adding to a `deque`

    Args:
        `filename` (str): A file to read

    Returns:
        `deque`: A deque (to be used as a stack) representing the tokenized file
    """
    stack = deque()
    contents = read_file(filename)
    active_comment = False

    for line in contents:
        # if a single-line comment or the whole line is a multi-line comment
        # , dispose of it/do nothing
        if is_single_comment(line) or is_full_ml_comment(line):
            continue
        # TODO: Handle actual mutli-line comments, including ones that start/end around actual tokens

    raise NotImplementedError
    return stack
