"""
Module with helper functions to parse, compile, and output files for tokens of a Jack program

Should unescape escaped tokens as well as form new structures based on the Jack Grammar
"""

from __future__ import annotations
from collections import deque
from typing import Callable, Iterable, Optional

import html

from constants import (
    EO_TOKEN_FILE,
    OPS,
    STATEMENT_TERMINATOR,
    VAR_DEC_START,
    VAR_DEC_END,
    LET_START,
    LET_END,
)

from tokenizer import parse_file


class CompilationEngine:
    """Takes a set of tokens or file and outputs an XML file of the fully analyzed syntax.

    Follows the Jack grammar:

        `class`: `class` `className` `'{'` `classVarDec*` `subroutineDec`* `'}'`

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

        `_filename` (str): The filename to which we write the compiled code.
        `_tokens` (deque[str]): All remaining tokens to be compiled.
            Is reduced by 1 token each time we `advance_token`.
        `_current_token` (str): The current token to be compiled.
            Updated by `advance_token` when necessary to move to the next token.

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

        # Automatically set the first token
        self.advance_token()

        # Create a default queue of compiled items
        self._compiled_tokens = deque()

    def advance_token(self) -> None:
        """Advances the currently active token

        If the tokens deque is empty when trying to advance, set the current token
        to an empty string.  This should only be an issue at the end of `compile_class`
        """

        try:
            self._current_token = self._tokens.popleft()
        except IndexError:
            self._current_token = ""

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

    def compile_var_dec(self) -> None:
        """Compiles a `var` declaration according to the varDec grammar

        `varDec`: `'var'` `type` `varName` (`',' varName`)*

        Will be called if `self._current_token` == `var` and we're in a subroutine body.
        """
        if self._current_token != "<keyword> var </keyword>\n":
            raise ValueError(f"{self._current_token} is not a var declaration")

        self._compiled_tokens.append(VAR_DEC_START)

        while self._current_token != STATEMENT_TERMINATOR:
            self._compiled_tokens.append(self._current_token)
            self.advance_token()

        self._compiled_tokens.append(self._current_token)  # statement terminator
        self._compiled_tokens.append(VAR_DEC_END)
        self.advance_token()

    def compile_statements(self, /) -> None:
        raise NotImplementedError

    def compile_let(self) -> None:
        """Compiles a `let` statement according to `letStatement` grammar

        `let varName` (`'['expression']'`)? `'=' expression ';'`

        Will be called if `self._current_token` == `let`
        """
        if self._current_token != "<keyword> let </keyword>\n":
            raise ValueError(f"{self._current_token} is not a let statement")

        self._compiled_tokens.append(LET_START)

        while self._current_token != STATEMENT_TERMINATOR:
            # as in `let i = 1;`
            # or `let arr[i] = 1;`
            if self._current_token in (
                "<symbol> = </symbol>\n",
                "<symbol> [ </symbol>\n",
            ):
                self._compiled_tokens.append(self._current_token)
                self.advance_token()
                self.compile_expression()
            else:
                self._compiled_tokens.append(self._current_token)
                self.advance_token()

        self._compiled_tokens.append(self._current_token)  # statement terminator
        self._compiled_tokens.append(LET_END)
        self.advance_token()

    def compile_if(self, /) -> None:
        raise NotImplementedError

    def compile_while(self, /) -> None:
        raise NotImplementedError

    def compile_do(self, /) -> None:
        raise NotImplementedError

    def compile_return(self, /) -> None:
        raise NotImplementedError

    def compile_expression(self, /) -> None:
        """Compiles an expression according to `expression` grammar

        `expression`: `term` (`op term`)*
        """

        # Always starts with a term
        self.compile_term()
        self.advance_token()

        # If the next token is an op, we continue to compile `op term`
        # and repeat until we run out of instances of (`op term`)
        while is_op(self._current_token):
            # Compile the `op`
            self._compiled_tokens.append(self._current_token)
            self.advance_token()
            # Compile the `term`
            self.compile_term()
            self.advance_token()

    def compile_term(self, /) -> None:
        raise NotImplementedError

    def compile_expression_list(self, /) -> None:
        raise NotImplementedError


# Maybe these should be in a separate module?
# Don't need to be in the class, as they don't need the state
def is_op(token: str) -> bool:
    """Return true if the passed token is an op

    `op`: `'+'`|`'-'`|`'*'`|`'/'`|`'&'`|`'|'`|`'<'`|`'>'`|`'='`

    Args:
        `token` (str): The token in the format `<symbol> token </symbol>`

    Returns:
        `bool`: If the token is an op
    """

    return token.split()[1] in OPS
