"""
Module with helper functions to parse, compile, and output files for tokens of a Jack program

Should unescape escaped tokens as well as form new structures based on the Jack Grammar
"""

from __future__ import annotations
from collections import deque
from typing import Callable, Iterable, Optional

import html

from constants import KEYWORDS, SYMBOLS, EO_TOKEN_FILE
from tokenizer import parse_file


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
        self,
        filename: str,
        tokens: Optional[Iterable[str]] = None,
        *,
        parse_func: Callable[[str], deque[str]] = parse_file,
    ) -> None:
        """Creates an instance of CompilationEngine

        Args:
            `filename` (str): The filename to which we will write the compiled code.
                If tokens is null, we also parse the file and create all tokens.
            `tokens` (Iterable[str] | None): An Iterable of tokens.
                If none, the `filename` will be passed to a `parse_func`
                to create the necessary tokens.
            `parse_func` (Callable[[str] , deque[str]]): Function used to parse tokens from
                `filename` if tokens are not provided. (default: `parse_file` from `tokenizer`)
        """
        self._filename = filename

        if tokens:
            self._tokens = deque(tokens)
        else:
            self._tokens = parse_func(filename)

    def compile_class(self, /) -> None:
        raise NotImplementedError

    def compile_class_var_dec(self, /) -> None:
        raise NotImplementedError

    def compile_subroutine_dec(self, /) -> None:
        raise NotImplementedError

    def compile_parameter_list(self, /) -> None:
        raise NotImplementedError

    def compile_subroutine_body(self, /) -> None:
        raise NotImplementedError

    def compile_var_dec(self, /) -> None:
        raise NotImplementedError

    def compile_statements(self, /) -> None:
        raise NotImplementedError

    def compile_let(self, /) -> None:
        raise NotImplementedError

    def compile_if(self, /) -> None:
        raise NotImplementedError

    def compile_while(self, /) -> None:
        raise NotImplementedError

    def compile_do(self, /) -> None:
        raise NotImplementedError

    def compile_return(self, /) -> None:
        raise NotImplementedError

    def compile_expression(self, /) -> None:
        raise NotImplementedError

    def compile_term(self, /) -> None:
        raise NotImplementedError

    def compile_expression_list(self, /) -> None:
        raise NotImplementedError


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
