"""
Module with helper functions to handle comments in a .jack file

Will remove single line comments denoted by '//' as well as
multi-line comments denoted by '/*' and '*/'
"""

from __future__ import annotations
from collections import deque

from constants import COMMENT, ML_COMMENT_START, ML_COMMENT_END


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

    return (
        line.startswith(ML_COMMENT_START)
        and line.endswith(ML_COMMENT_END)
        and line.count(ML_COMMENT_END) == 1
    )


def handle_complex_comments(line: str, active_comment: bool) -> tuple[str, bool]:
    """Modify current line based on where it contains a comment.

    Args:
        `line` (str): The unparsed .jack code line

    Returns:
        `str`: The modified line
        `bool`: A confirmation that we are either in a multi-line comment or not
    """

    # If not already an active comment, we can remove all comments in the line
    if not active_comment:
        while (index := line.find(ML_COMMENT_START)) > -1:
            if (end_index := line.find(ML_COMMENT_END)) > -1:
                # If a comment ends, then we can remove that whole comment
                # And confirm that the comment has ended
                line_to_remove = line[index : end_index + len(ML_COMMENT_END)]
                active_comment = False
            else:
                # Otherwise, just remove everything from the start of the comment forward
                # And confirm that a comment is active
                line_to_remove = line[index:]
                active_comment = True
            line = line.replace(line_to_remove, "")

        # Also don't forget to remove a single-line comment that maybe occurs after valid code
        if (index := line.find(COMMENT)) > -1:
            line = line[:index]
    else:
        # If an active comment, find the first closing and remove, then recurse
        if (end_index := line.find(ML_COMMENT_END)) > -1:
            line_to_remove = line[: end_index + len(ML_COMMENT_END)]
            active_comment = False
            line = line.replace(line_to_remove, "")
            line, active_comment = handle_complex_comments(line, active_comment)
        else:
            # If there's no ending, just remove the whole line
            line = ""

    # Strip just in case there is any remaining whitespace
    return line.strip(), active_comment


def remove_comments(file_contents: list[str]) -> deque[str]:
    """Process a file's contents, removing all comments and putting the remmainder in a deque

    Args:
        `file_contents` (str): The file's contents previously split on a newlines

    Returns:
        `deque[str]`: The file's contents as a stack, with all comments removed
    """

    stack = deque()
    active_comment = False

    for line in file_contents:
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
