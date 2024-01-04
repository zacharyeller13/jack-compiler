"""
Module with functions to write tokens to <filename>T.xml

Should just process a deque with tokens and write them to the file
"""

from __future__ import annotations
from collections import deque
from io import TextIOWrapper

from tokenizer import classify_token, escape_token


def write_tokens_file(filename: str, tokens: deque[str]) -> None:
    with open(f"{filename}T.xml", "w", encoding="UTF-8") as f:
        write_opener(f)
        for token in tokens:
            write_token(f, token)
        write_closer(f)


def write_opener(file_ptr: TextIOWrapper) -> None:
    """Writes the opening to a token file"""
    file_ptr.write("<tokens>\n")


def write_closer(file_ptr: TextIOWrapper) -> None:
    """Writes the closing to a token file"""
    file_ptr.write("</tokens>")


def write_token(file_ptr: TextIOWrapper, token: str) -> None:
    """Writes the token to file

    Args:
        `file_ptr` (TextIOWrapper): The currently open File
        `token` (str): The current token to write
    """

    template = "<{token_type}> {token} </{token_type}>\n"
    file_ptr.write(template.format(token_type=classify_token(token), token=escape_token(token)))
