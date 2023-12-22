"""
Module with functions to write tokens to <filename>T.xml

Should just process a deque with tokens and write them to the file
"""

from __future__ import annotations
from collections import deque


def write_tokens_file(filename: str, tokens: deque[str]) -> None:
    with open(filename, "w", encoding="UTF-8") as f:
        f.writelines(f"{token}\n" for token in tokens)
