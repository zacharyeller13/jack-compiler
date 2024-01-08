"""
Module with helper functions to parse and tokenize a .jack file

Should ignore newlines, spaces, and comments and then parse the remaining
pieces of a file into valid Jack tokens
"""
from __future__ import annotations
from collections import deque

import html
import re

from comment_handler import remove_comments
from constants import KEYWORDS, SYMBOLS, TOKEN_TEMPLATE


def is_symbol(char: str) -> bool:
    """Return true if char is a `SYMBOL`

    Args:
        `char`: Character that may be a symbol

    Returns:
        `bool`: True if char in `SYMBOLS` else False
    """

    return char in SYMBOLS


def is_string_constant(word: str) -> bool:
    """Return true if word is a string constant

    Args:
        `word`: A string

    Returns:
        `bool`: True if starts and ends with " denoting a string constant
    """

    return word.startswith('"') and word.endswith('"') and word.count('"') == 2


def is_keyword(word: str) -> bool:
    """Return true if the word/token is a reserved keyword

    Args:
        `word` (str): A string

    Returns:
        `bool`: True if in the set of `KEYWORDS`, else False
    """

    return word in KEYWORDS


def classify_token(token: str) -> str:
    """Return the type of token

    Args:
        `token` (str): The current token to classify

    Returns:
        `str`: The type/classification of the token.  One of:
            - keyword
            - symbol
            - integerConstant
            - stringConstant
            - identifier
    """

    if is_keyword(token):
        return "keyword"
    if is_symbol(token):
        return "symbol"
    if token.isdigit():
        return "integerConstant"
    if is_string_constant(token):
        return "stringConstant"
    return "identifier"


def escape_token(token: str) -> str:
    """Escape reserved symbols such as `<` to `%lt;` and replace `"` in any string literals

    Args:
        `token` (str): The token to escape. Escaping really only for one of:
        `<`, `>`, and `&`

    Returns:
        `str`: An escaped version of the char. One of:
        `&lt;`, `&gt;`, and `&amp;` or the token itself with `"` removed
    """

    return html.escape(token.replace('"', ""))


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

    tokens = deque()

    while stack:
        # Pop left so that we get line 1 first, line 2 second, etc.
        tokens.extend(tokenize_line(stack.popleft()))

    return tokens


def tokenize_line(line: str) -> deque[str]:
    """Process a single Jack code line, splitting into individual tokens

    Args:
        `line` (str): The Jack code line

    Returns:
        `deque[str]`: A stack of the tokens.
            Stack/deque because it's optimized for repeated adds
    """

    if not line:
        return deque(line)

    pattern = re.compile(r'"[^"]*?"|[^"\s]+')
    split_line = pattern.findall(line)
    tokens = deque()

    # for word in split_line:
    #     if is_string_constant(word):
    #         tokens.append(word)
    #     elif sum(sym in word for sym in SYMBOLS) > 0:
    #         tokens.extend(tokenize_symbols(word))
    #     else:
    #         tokens.append(word)

    for word in split_line:
        if is_string_constant(word):
            tokens.append(
                TOKEN_TEMPLATE.format(
                    token_type=classify_token(word), token=escape_token(word)
                )
            )
        elif sum(sym in word for sym in SYMBOLS) > 0:
            tokens.extend(tokenize_symbols(word))
        else:
            tokens.append(
                TOKEN_TEMPLATE.format(
                    token_type=classify_token(word), token=escape_token(word)
                )
            )

    return tokens


def tokenize_symbols(word: str) -> deque[str]:
    """Process a single string that contains on or more `SYMBOLS`, splitting it into individual tokens.
        `<`, `>`, `"` and `&` are output as `&lt;`, `&gt;`, `&quot;`, and `&amp;`

    Args:
        `word` (str): The string to be tokenized

    Returns:
        `deque[str]`: A stack of tokens
    """

    tokens = deque()
    token = ""

    for char in word:
        if not is_symbol(char):
            token += char
        else:
            if token:
                tokens.append(
                    TOKEN_TEMPLATE.format(
                        token_type=classify_token(token), token=escape_token(token)
                    )
                )
                token = ""
            tokens.append(
                TOKEN_TEMPLATE.format(
                    token_type=classify_token(char), token=escape_token(char)
                )
            )

    # Final add to tokens if we have a symbol of some kind at the end of the word
    if token:
        tokens.append(
            TOKEN_TEMPLATE.format(
                token_type=classify_token(token), token=escape_token(token)
            )
        )

    return tokens


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
    tokens = tokenize(stack)

    return tokens
