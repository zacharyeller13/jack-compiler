"""
Module with functions to write tokens to <filename>T.xml

Should just process a deque with tokens and write them to the file
"""

from __future__ import annotations
from collections import deque
from io import TextIOWrapper

from constants import EO_TOKEN_FILE


def write_tokens_file(filename: str, tokens: deque[str]) -> None:
    with open(f"{filename}T.xml", "w", encoding="UTF-8") as f:
        write_opener(f)
        f.writelines(tokens)
        write_closer(f)


def write_opener(file_ptr: TextIOWrapper) -> None:
    """Writes the opening to a token file"""
    file_ptr.write("<tokens>\n")


def write_closer(file_ptr: TextIOWrapper) -> None:
    """Writes the closing to a token file"""
    file_ptr.write(EO_TOKEN_FILE)
