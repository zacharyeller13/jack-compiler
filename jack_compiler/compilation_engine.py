"""
Module with helper functions to parse, compile, and output files for tokens of a Jack program

Should unescape escaped tokens as well as form new structures based on the Jack Grammar
"""

from __future__ import annotations
from collections import deque
from typing import Callable, Iterable, Optional

import html

from constants import (
    CLOSE_BRACE,
    DO_END,
    DO_START,
    END_IF,
    EXPRESSION_END,
    EXPRESSION_START,
    IF_STATEMENT,
    MEMBER_ACCESSOR,
    OPEN_PAREN,
    OPS,
    RETURN_END,
    RETURN_START,
    STATEMENT_TERMINATOR,
    TERM_END,
    TERM_START,
    VAR_DEC_START,
    VAR_DEC_END,
    LET_START,
    LET_END,
    CLOSE_PAREN,
    EXPRESSION_LIST_START,
    EXPRESSION_LIST_END,
    WHILE_END,
    WHILE_START,
)

from jack_compiler.symbol_table import SymbolTable
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

        `_files` (Iterable[str]): List of files to be compiled by the engine
        `_current_filename` (str): The filename to which we write the current code
            being compiled.
        `_tokens` (deque[str]): All remaining tokens to be compiled.
            Is reduced by 1 token each time we `advance_token`.
        `_current_token` (str): The current token to be compiled.
            Updated by `advance_token` when necessary to move to the next token.
        `_symbol_table` (SymbolTable): The symbol table being using for this
            engine.
    """

    def __init__(
        self,
        files: Iterable[str] | str,
        *,
        tokens: Optional[Iterable[str]] = None,
        parse_func: Callable[[str], deque[str]] = parse_file,
    ) -> None:
        """Creates an instance of CompilationEngine

        Args:
            `files` (Iterable[str] | str): The list of files to be compiled.
                If tokens is null, we will parse the each file and create all tokens.
                If a single filename is provided, we just parse the single file
            `tokens` (Iterable[str] | None): An Iterable of tokens.
                If none, each file in `files` will be passed to a `parse_func`
                to create the necessary tokens.
            `parse_func` (Callable[[str] , deque[str]]): Function used to parse tokens from
                `files` if tokens are not provided. (default: `parse_file` from `tokenizer`)
        """

        # Setup our parsing function
        self.parse_func = parse_func
        # Ensure self._files will always be an iterable
        self._files = deque([files]) if isinstance(files, str) else deque(files)
        # This is a little bit of extra work if a files is a string, but oh well
        self._current_filename = self._files.popleft()
        # Setup our starting SymbolTable
        self._symbol_table = SymbolTable()

        # If tokens are given, we assume that they are for the first file
        if tokens:
            self._tokens = deque(tokens)
        else:
            self._tokens = parse_func(self._current_filename)

        # Create a default queue to hold compiled items
        self._compiled_tokens = deque()

        # Automatically set the first token
        # We don't need to advance twice, b/c the first "token" will only be '<token>\n"
        # when we write to a file.  Otherwise we just start with the first token
        self.advance_token()

    def compile_all(self) -> None:
        """Do all compilation activities for every file in `_files` and
        write to output file(s)
        """

        # We have already set the first batch of tokens so we just compile them
        # They should always start with 'class'
        self.compile_class()
        self.write_compilation_file()
        self._compiled_tokens.clear()

        # Should exit when self._files == deque([])
        while self._files:
            self._current_filename = self._files.popleft()
            self._tokens = self.parse_func(self._current_filename)
            # We need to set first token
            self.advance_token()
            self.compile_class()
            self.write_compilation_file()
            self._compiled_tokens.clear()

    def write_compilation_file(self) -> None:
        with open(
            f"{self._current_filename[: -len('.jack')]}.xml", "w", encoding="UTF-8"
        ) as f:
            f.writelines(self._compiled_tokens)

    def advance_token(self) -> None:
        """Advances the currently active token

        If the tokens deque is empty when trying to advance, set the current token
        to an empty string.  This should only be an issue at the end of `compile_class`
        """

        try:
            self._current_token = self._tokens.popleft()
        except IndexError:
            self._current_token = None

    def peek_next_token(self) -> str | None:
        """Peek to the next token

        Returns:
            `str` | `None`: The token if there is one, None is the queue is empty
        """

        try:
            return self._tokens[0]
        except IndexError:
            return None

    def compile_class(self) -> None:
        """Compile a full class (basically the same as a whole file):

        `'class' className '{' classVarDec* subroutineDec* '}'`
        """

        self._compiled_tokens.append("<class>\n")
        # class keyword
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # class name
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # open brace
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        while self._current_token != CLOSE_BRACE:
            if self._current_token in (
                "<keyword> static </keyword>\n",
                "<keyword> field </keyword>\n",
            ):
                self.compile_class_var_dec()
            else:
                self.compile_subroutine_dec()

        # close brace
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        self._compiled_tokens.append("</class>\n")

    def compile_class_var_dec(self) -> None:
        """Compile class variable declarations according to grammar:

        `('static'|'field') type varName (',' varName)* ';'`
        """

        # classVarDec
        self._compiled_tokens.append("<classVarDec>\n")

        # static or field
        static_field = self._current_token.split()[1]
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # type
        data_type = self._current_token.split()[1]
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # (',' varName)*
        while self._current_token != STATEMENT_TERMINATOR:
            # ,
            if self._current_token == "<symbol> , </symbol>\n":
                self._compiled_tokens.append(self._current_token)
                self.advance_token()

            # varName
            # Add to symbol table
            identifier_name = self._current_token.split()[1]
            self._symbol_table.define(
                name=identifier_name, data_type=data_type, category=static_field
            )
            identifier = " ".join(
                (
                    f"<identifier category='{static_field}'",
                    f"index={self._symbol_table.class_table.get(identifier_name).index}",
                    "usage='declared'>",
                    identifier_name,
                    "</identifier>\n",
                )
            )
            # Output to file
            self._compiled_tokens.append(identifier)
            self.advance_token()

        # ;
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # /classVarDec
        self._compiled_tokens.append("</classVarDec>\n")

    def compile_subroutine_dec(self) -> None:
        """Compile a subroutine declaration according to grammar:

        `('constructor' | 'function' | 'method') ('void' | type) subroutineName
        '(' parameterList ')' subroutineBody
        """

        # TODO: For constructor and method
        # If a constructor, clear both tables.
        # If a method, add the implicit `this` argument to the subroutine table
        # Currently, no way to know what the current type of `this` would be
        self._compiled_tokens.append("<subroutineDec>\n")

        # constructor/function/method
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # void/type
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # subroutineName

        # Add to symbol table
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # open paren
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        self.compile_parameter_list()

        # close paren
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        self.compile_subroutine_body()

        self._compiled_tokens.append("</subroutineDec>\n")

    def compile_parameter_list(self) -> None:
        """Compile a subroutine's parameter list:

        `( (type varName) (',' type varName)* )?`
        """

        self._compiled_tokens.append("<parameterList>\n")

        # symbol table category
        category = "argument"

        while self._current_token != CLOSE_PAREN:
            if self._current_token == "<symbol> , </symbol>\n":
                self._compiled_tokens.append(self._current_token)
                self.advance_token()

            # type
            data_type = self._current_token.split()[1]
            self._compiled_tokens.append(self._current_token)
            self.advance_token()

            # varName
            identifier_name = self._current_token.split()[1]
            self._compiled_tokens.append(self._current_token)
            self.advance_token()

        self._compiled_tokens.append("</parameterList>\n")

    def compile_subroutine_body(self) -> None:
        """Compile a subroutine body according to grammar:

        `'{' varDec* statements '}'`
        """

        self._compiled_tokens.append("<subroutineBody>\n")

        # clear subroutine symbol table
        # As we're starting a new local scope
        self._symbol_table.start_subroutine()

        # Compile open brace
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        while self._current_token != CLOSE_BRACE:
            if self._current_token == "<keyword> var </keyword>\n":
                self.compile_var_dec()
            else:
                self.compile_statements()

        # Compile close brace
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        self._compiled_tokens.append("</subroutineBody>\n")

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

    def compile_statements(self) -> None:
        """Compiles multiple statements

        `statement`*

        Occurs in the following cases:
            `subroutineBody`
            `ifStatement` (including when there is an `else` part)
            `whileStatement`

        Raises:
            `ValueError`: If the current token is not a statement
        """

        self._compiled_tokens.append("<statements>\n")

        while self._current_token != CLOSE_BRACE:
            if self._current_token == "<keyword> let </keyword>\n":
                self.compile_let()
            elif self._current_token == "<keyword> if </keyword>\n":
                self.compile_if()
            elif self._current_token == "<keyword> while </keyword>\n":
                self.compile_while()
            elif self._current_token == "<keyword> do </keyword>\n":
                self.compile_do()
            elif self._current_token == "<keyword> return </keyword>\n":
                self.compile_return()
            else:
                raise ValueError(
                    f"Current Token {self._current_token} is not a statement"
                )

        self._compiled_tokens.append("</statements>\n")

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
                # append '=' or '['
                self._compiled_tokens.append(self._current_token)
                self.advance_token()
                # append right side after '='
                # or append the expression between '[' and ']'
                self.compile_expression()
            else:
                self._compiled_tokens.append(self._current_token)
                self.advance_token()

        self._compiled_tokens.append(self._current_token)  # statement terminator
        self._compiled_tokens.append(LET_END)
        self.advance_token()

    def compile_if(self) -> None:
        """Compiles an if statement according to the grammar

        `if '(' expression ')' '{' statements '}' (else '{' statements '}')?`
        """

        if self._current_token != "<keyword> if </keyword>\n":
            raise ValueError(f"{self._current_token} is not an if keyword")

        # <ifStatement>
        self._compiled_tokens.append(IF_STATEMENT)
        # <keyword> if </keyword>
        self._compiled_tokens.append(self._current_token)
        self.advance_token()
        # open paren
        self._compiled_tokens.append(self._current_token)
        self.advance_token()
        # expression
        self.compile_expression()
        # close paren
        self._compiled_tokens.append(self._current_token)
        self.advance_token()
        # open curly brace
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # statements
        self.compile_statements()

        # close curly brace
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # optional else statement
        if self._current_token == "<keyword> else </keyword>\n":
            # compile the else bit
            self._compiled_tokens.append(self._current_token)
            self.advance_token()
            # open curly brace
            self._compiled_tokens.append(self._current_token)
            self.advance_token()
            # statements
            self.compile_statements()

            # close curly brace
            self._compiled_tokens.append(self._current_token)
            self.advance_token()

        self._compiled_tokens.append(END_IF)

    def compile_while(self) -> None:
        """Compiles a while statement according to the grammar

        `while '(' expression ')' '{' statements '}'`
        """

        # <whileStatement>
        self._compiled_tokens.append(WHILE_START)
        # keyword while
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # open paren
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        self.compile_expression()

        # close paren
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # open brace
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        self.compile_statements()

        # close brace
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # end while
        self._compiled_tokens.append(WHILE_END)

    def compile_do(self) -> None:
        """Compiles a do statement according to the grammar

        `do` subroutineCall `';'`
        """

        # <doStatement>
        self._compiled_tokens.append(DO_START)
        # <keyword> do </keyword>
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # Compile subroutine call
        # identifier(.identifier)?(expressionList)
        # identifier
        self._compiled_tokens.append(self._current_token)
        self.advance_token()
        # .identifier?
        if self._current_token == "<symbol> . </symbol>\n":
            self._compiled_tokens.append(self._current_token)
            self.advance_token()
            self._compiled_tokens.append(self._current_token)
            self.advance_token()

        # open paren
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        self.compile_expression_list()

        # close paren
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # We should now be at the ';'
        self._compiled_tokens.append(self._current_token)
        self._compiled_tokens.append(DO_END)
        self.advance_token()

    def compile_return(self) -> None:
        """Compiles a return statement according to the grammar

        `return`: `expression`? ';'
        """

        self._compiled_tokens.append(RETURN_START)
        # <keyword> return </keyword>
        self._compiled_tokens.append(self._current_token)
        self.advance_token()

        # This means we have an expression to compile
        if self._current_token != STATEMENT_TERMINATOR:
            self.compile_expression()

        # We are now already at the ';'
        self._compiled_tokens.append(self._current_token)
        self._compiled_tokens.append(RETURN_END)
        self.advance_token()

    def compile_expression(self) -> None:
        """Compiles an expression according to `expression` grammar

        `expression`: `term` (`op term`)*
        """

        self._compiled_tokens.append(EXPRESSION_START)

        # Always starts with a term
        self.compile_term()

        # If the next token is an op, we continue to compile `op term`
        # and repeat until we run out of instances of (`op term`)
        while is_op(self._current_token):
            # Compile the `op`
            self._compiled_tokens.append(self._current_token)
            self.advance_token()
            # Compile the `term`, which includes advancing
            self.compile_term()

        self._compiled_tokens.append(EXPRESSION_END)

    def compile_term(self) -> None:
        """Compiles a term according to `term` grammar

        `term`: `integerConstant` | `stringConstant` | `keywordConstant` | `varName` | `varName'[' expression ']'` |
          `subroutineCall` | `'(' expression ')'` | `unaryOp term`
        """

        # if not identifier
        # compile, advance, return
        if not is_identifier(self._current_token):
            # integerConstant, stringConstant, keywordConstant
            self._compiled_tokens.append(TERM_START)
            if self._current_token in (
                "<symbol> ~ </symbol>\n",
                "<symbol> - </symbol>\n",
            ):
                self._compiled_tokens.append(self._current_token)
                self.advance_token()
                self.compile_term()

            # '(' expression ')'
            elif self._current_token == OPEN_PAREN:
                self._compiled_tokens.append(self._current_token)
                self.advance_token()

                self.compile_expression()

                assert self._current_token == CLOSE_PAREN
                self._compiled_tokens.append(self._current_token)
                self.advance_token()

            # Anything else
            else:
                self._compiled_tokens.append(self._current_token)
                self.advance_token()

            self._compiled_tokens.append(TERM_END)
            # self.advance_token()
            return

        # If is identifier, distinguish between variable, array entry, subroutine call
        # lookahead, compile variable, array access, subroutine call accordingly
        # TODO: Also, if var | argument | static | field; output index from symbol table
        self._compiled_tokens.append(TERM_START)
        # peek at next token
        next_token = self.peek_next_token()
        # array access
        if next_token == "<symbol> [ </symbol>\n":
            # identifier
            self._compiled_tokens.append(self._current_token)
            # advance to '[' compile and advance
            self.advance_token()
            self._compiled_tokens.append(self._current_token)
            self.advance_token()
            # now compile the expression inside of '[' and ']'
            self.compile_expression()
            # compile ending ']'
            self._compiled_tokens.append(self._current_token)
            self.advance_token()
        # normal subroutine call
        elif next_token == OPEN_PAREN:
            # identifier
            self._compiled_tokens.append(self._current_token)
            # advance to '(' compile and advance
            self.advance_token()
            self._compiled_tokens.append(self._current_token)
            self.advance_token()
            # now compile the expression inside of '(' and ')'
            self.compile_expression_list()
            # compile ending ')'
            self._compiled_tokens.append(self._current_token)
            self.advance_token()
        # className.subroutineName || varName.subroutineName
        elif next_token == MEMBER_ACCESSOR:
            # identifier
            self._compiled_tokens.append(self._current_token)
            self.advance_token()
            # member accessor
            self._compiled_tokens.append(self._current_token)
            self.advance_token()
            # identifier
            self._compiled_tokens.append(self._current_token)
            self.advance_token()
            # '(' compile and advance
            self._compiled_tokens.append(self._current_token)
            self.advance_token()

            self.compile_expression_list()

            # compile ending ')'
            self._compiled_tokens.append(self._current_token)
            self.advance_token()

        # normal variable
        else:
            self._compiled_tokens.append(self._current_token)
            self.advance_token()

        self._compiled_tokens.append(TERM_END)
        return

    def compile_expression_list(self) -> None:
        """Compile an expression list which really only happens in a `subroutineCall`

        (`expression (',' expression)`*)?
        """

        # ( Open Paren
        # self._compiled_tokens.append(self._current_token)
        # self.advance_token()
        # open paren should already be compiled!

        # expression(s)
        self._compiled_tokens.append(EXPRESSION_LIST_START)
        # while we're still inside the parens
        while self._current_token != CLOSE_PAREN:
            if self._current_token == "<symbol> , </symbol>\n":
                self._compiled_tokens.append(self._current_token)
                self.advance_token()

            self.compile_expression()

        self._compiled_tokens.append(EXPRESSION_LIST_END)

        # ) Close paren
        # self._compiled_tokens.append(self._current_token)
        # self.advance_token()
        # close paren should already be compiled


# Maybe these should be in a separate module?
# Don't need to be in the class, as they don't need the state
def is_op(token: Optional[str]) -> bool:
    """Return true if the passed token is an op

    `op`: `'+'`|`'-'`|`'*'`|`'/'`|`'&'`|`'|'`|`'<'`|`'>'`|`'='`

    Args:
        `token` (str): The token in the format `<symbol> token </symbol>`

    Returns:
        `bool`: If the token is an op
    """

    # If we have an empty string or None
    if not token:
        return False

    return html.unescape(token.split()[1]) in OPS


def is_identifier(token: Optional[str]) -> bool:
    """Return true if passed token is an identifier

    Args:
        `token` (str): The token in the format `<identifier> token </identifier>`

    Returns:
        `bool`: If the token is an identifier
    """

    # If we have an empty string or None
    if not token:
        return False

    return token.split()[0] == "<identifier>"
