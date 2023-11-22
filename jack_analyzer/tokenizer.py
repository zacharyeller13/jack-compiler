"""
Module with helper functions to parse and tokenize a .jack file

Should ignore newlines, spaces, and comments and then parse the remaining
pieces of a file into valid Jack tokens
"""
from __future__ import annotations
from collections import deque

from comment_handler import (
    is_single_comment,
    is_full_ml_comment,
    handle_complex_comments,
)


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

        line, active_comment = handle_complex_comments(line, active_comment)
        # if there's no active comment and it's not an empty line, we need to process it
        # So add it to the stack
        if not active_comment and line != "":
            stack.append(line)

    return stack
