"""
Module with helper functions to parse the `*T.xml` token files for a Jack program

Should unescape escaped tokens as well as form new structures based on the Jack Grammar
"""

from __future__ import annotations
from collections import deque

import html
from io import TextIOWrapper
from typing import Iterable

from constants import KEYWORDS, SYMBOLS, EO_TOKEN_FILE
from tokenizer import parse_file


# TODO: decision - Create a class with methods to match the spec (compile_xxx methods)
# And maintain state for each file? Should make it easier than passing file pointers around
# between functions


class CompilationEngine:
    """Takes a set of tokens or filestream and outputs an XML file of the fully analyzed syntax.

    Follows the Jack grammar:

        `class`: `class` `className` `'{'` `classVarDec*` `subrouteinDec`* `'}'`

        `classVarDec`: (`static` | `field`) `type` `varName` (`',' varName`)* `';'`

        `type`: `int` | `char` | `boolean` | `className`

        `subroutineDec`: (`constructor`|`function`|`method`) (`'void'` | `type`) `subroutineName`
            `'('` `parameterList` `')'` `subroutineBody`

        `parameterList`: ( `(type varName)` (`',' varName`)* )?

        `subroutineBody`: `'{'` `varDec`* `statements` `'}'`

        `varDec`: `'var'` `type` `varName` (`',' varName`)*

        `className`: identifier

        `subroutineName`: identifier

        `varName`: identifier

        `statements`: `statement`*

        `statement`: `letStatement`|`ifStatement`|`whileStatement`|`doStatement`|`returnStatement`

    Attributes:

        TODO: List attributes etc.

    """

    def __init__(
        self, tokens: deque[str], filestream: TextIOWrapper | None = None
    ) -> None:
        """Creates an instance of CompilationEngine

        Args:
            `tokens` (deque[str] | None): A deque of tokens . If none, the `filestream` will be used
                to create the tokens
            `filestream` (TextIOWrapper | None): If tokens is null, parse the filestream and create
                all tokens
        """
        self._tokens = tokens


def compile_class(token_file: str) -> None:
    """Write the full class.  In Jack all files are also classes,
    so we should be able to just write the opener and closer without actually analyzing what starts/ends the file
    and then let the other functions/methods handle their respective parts of the grammar

    Args:
        `token_file` (str): A token file contain all of the class's tokens
    """

    with open(token_file, "r", encoding="UTF-8") as reader, open(
        token_file.replace("T.xml", ".xml"), "w", encoding="UTF-8"
    ) as writer:
        writer.write("<class>\n")

        # Skip the first line because it is guaranteed to be "<tokens>"
        # Next 3 lines are guaranteed? to be "class", className
        # , and symbol opener, so just write those also?

        next(reader)  # skip class declaration
        class_name = reader.readline()
        next(reader)  # skip '{'
        writer.write(f"{class_name}\n<symbol> {{ </symbol>")

        current_token = reader.readline()

        while current_token != EO_TOKEN_FILE:
            # Handle keywords
            if current_token.startswith("<keyword>"):
                writer.write(current_token)
            # TODO: Analyze and write program parts
            current_token = reader.readline()

        # We're done parsing this file, close the class and exit the function
        writer.write("</class>")
