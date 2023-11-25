"""
Module with helper functions to parse and tokenize a .jack file

Should ignore newlines, spaces, and comments and then parse the remaining
pieces of a file into valid Jack tokens
"""
from __future__ import annotations
from collections import deque

from comment_handler import remove_comments


def tokenize(stack: deque[str]) -> deque[str]:
    """Process a stack of Jack code lines, splitting lines into individual tokens

    Args:
        `stack` (deque[str]): The Jack code lines, with comments already removed
    
    Returns:
        `deque[str]`: A stack of Jack tokens
    """

    # Stack is empty
    if not stack:
        return stack
    
    tokenized_stack = deque()

    while stack:
        # Pop left so that we get line 1 first, line 2 second, etc.
        tokenized_stack.append(stack.popleft())

    return tokenized_stack

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


def parse_file(filename: str) -> deque[str]:
    """Read a .jack file line by line, parsing as necessary and adding to a `deque`

    Args:
        `filename` (str): A file to read

    Returns:
        `deque[str]`: A deque (to be used as a stack) representing the tokenized file
    """

    contents = read_file(filename)
    stack = remove_comments(contents)

    # TODO: Pop items from stack, analyze if they are token by themselves or split into token parts

    return stack
