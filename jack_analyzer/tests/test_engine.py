"""
Tests for Compilation Engine
"""

from __future__ import annotations
from collections import deque
from pytest import fixture

from compilation_engine import CompilationEngine, is_op
from constants import (
    EXPRESSION_END,
    EXPRESSION_START,
    LET_END,
    LET_START,
    STATEMENT_TERMINATOR,
    VAR_DEC_START,
    VAR_DEC_END,
    TERM_START,
    TERM_END,
)


@fixture
def tokens():
    return [
        "<keyword> var </keyword>\n",
        "<keyword> int </keyword>\n",
        "<identifier> i </identifier>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> i </identifier>\n",
        "<symbol> = </symbol>\n",
        "<integerConstant> 0 </integerConstant>\n",
        "<symbol> ; </symbol>\n",
    ]


@fixture
def compiled_var_dec():
    return deque(
        [
            VAR_DEC_START,
            "<keyword> var </keyword>\n",
            "<keyword> int </keyword>\n",
            "<identifier> i </identifier>\n",
            "<symbol> ; </symbol>\n",
            VAR_DEC_END,
        ]
    )


@fixture
def compiled_var_dec_long():
    return deque(
        [
            VAR_DEC_START,
            "<keyword> var </keyword>\n",
            "<keyword> int </keyword>\n",
            "<identifier> i </identifier>\n",
            "<symbol> , </symbol>\n",
            "<identifier> j </identifier>\n",
            "<symbol> ; </symbol>\n",
            VAR_DEC_END,
        ]
    )


@fixture
def var_dec_long():
    return [
        "<keyword> var </keyword>\n",
        "<keyword> int </keyword>\n",
        "<identifier> i </identifier>\n",
        "<symbol> , </symbol>\n",
        "<identifier> j </identifier>\n",
        "<symbol> ; </symbol>\n",
    ]


@fixture
def expression_tokens():
    """As in `let i = 1 + 2;`"""
    return [
        "<integerConstant> 1 </integerConstant>\n",
        "<symbol> + </symbol>\n",
        "<integerConstant> 2 </integerConstant>\n",
    ]


@fixture
def compiled_expression():
    return deque(
        [
            "<expression>\n",
            TERM_START,
            "<integerConstant> 1 </integerConstant>\n",
            TERM_END,
            "<symbol> + </symbol>\n",
            TERM_START,
            "<integerConstant> 2 </integerConstant>\n",
            TERM_END,
            "</expression>\n",
        ]
    )


@fixture
def term_non_identifier():
    return ["<integerConstant> 1 </integerConstant>\n"]


@fixture
def compiled_term_non_identifier():
    return deque([TERM_START, "<integerConstant> 1 </integerConstant>\n", TERM_END])


@fixture
def let_statement_array_accessor():
    # let arr[i] = 1;
    return [
        "<keyword> let </keyword>\n",
        "<identifier> arr </identifier>\n",
        "<symbol> [ </symbol>\n",
        "<identifier> i </identifier>\n",
        "<symbol> ] </symbol>\n",
        "<symbol> = </symbol>\n",
        "<integerConstant> 1 </integerConstant>\n",
        STATEMENT_TERMINATOR,
    ]


@fixture
def compiled_let_statement_array_accessor():
    # let arr[i] = 1;
    return deque(
        [
            LET_START,
            "<keyword> let </keyword>\n",
            "<identifier> arr </identifier>\n",
            "<symbol> [ </symbol>\n",
            EXPRESSION_START,
            TERM_START,
            "<identifier> i </identifier>\n",
            TERM_END,
            EXPRESSION_END,
            "<symbol> ] </symbol>\n",
            "<symbol> = </symbol>\n",
            EXPRESSION_START,
            TERM_START,
            "<integerConstant> 1 </integerConstant>\n",
            TERM_END,
            EXPRESSION_END,
            STATEMENT_TERMINATOR,
            LET_END,
        ]
    )


@fixture
def engine(tokens) -> CompilationEngine:
    return CompilationEngine("test", tokens)


@fixture
def test_return_statement():
    return ["<keyword> return </keyword>\n", "<symbol> ; </symbol>\n"]


def test_constructor(tokens, engine) -> None:
    assert isinstance(engine, CompilationEngine)
    assert engine._tokens == deque(tokens[1:])
    assert engine._filename == "test"


def test_constructor_no_tokens(tokens) -> None:
    engine = CompilationEngine("test", tokens=None, parse_func=lambda _: deque(tokens))
    assert isinstance(engine, CompilationEngine)
    assert engine._tokens == deque(tokens[1:])
    assert engine._filename == "test"


def test_advance_token(tokens, engine) -> None:
    assert engine._current_token == tokens[0] == "<keyword> var </keyword>\n"
    engine.advance_token()
    assert engine._current_token == tokens[1] == "<keyword> int </keyword>\n"


def test_compile_var_dec(engine, compiled_var_dec) -> None:
    engine.compile_var_dec()
    assert engine._compiled_tokens == compiled_var_dec


def test_compile_var_dec_long(var_dec_long, compiled_var_dec_long) -> None:
    engine = CompilationEngine("test", var_dec_long)
    engine.compile_var_dec()
    assert engine._compiled_tokens == compiled_var_dec_long


def test_expression(expression_tokens, compiled_expression) -> None:
    engine = CompilationEngine("test", expression_tokens)
    engine.compile_expression()
    assert engine._compiled_tokens == compiled_expression


def test_is_op() -> None:
    assert is_op("<symbol> + </symbol>\n")


def test_term_non_identifier(term_non_identifier, compiled_term_non_identifier) -> None:
    engine = CompilationEngine("test", term_non_identifier)
    engine.compile_term()
    assert engine._compiled_tokens == compiled_term_non_identifier

@fixture
def term_unary_op():
    return [
        "<symbol> ~ </symbol>\n",
        "<identifier> a </identifier>\n",
    ]

@fixture
def compiled_term_unary_op():
    return deque([
        "<term>\n",
        "<symbol> ~ </symbol>\n",
        "<term>\n",
        "<identifier> a </identifier>\n",
        "</term>\n",
        "</term>\n",
    ])

def test_term_unary_op(term_unary_op, compiled_term_unary_op) -> None:
    engine = CompilationEngine("test", term_unary_op)
    engine.compile_term()
    assert engine._compiled_tokens == compiled_term_unary_op

def test_let_statement(
    let_statement_array_accessor, compiled_let_statement_array_accessor
):
    engine = CompilationEngine("test", let_statement_array_accessor)
    engine.compile_let()
    assert engine._compiled_tokens == compiled_let_statement_array_accessor


@fixture
def expression_list_tokens() -> list[str]:
    return [
        "<symbol> ( </symbol>\n",
        "<integerConstant> 2 </integerConstant>\n",
        "<symbol> , </symbol>\n",
        "<identifier> x </identifier>\n",
        "<symbol> ) </symbol>\n",
    ]


@fixture
def compiled_expression_list_tokens() -> list[str]:
    return deque(
        [
            "<symbol> ( </symbol>\n",
            "<expressionList>\n",
            "<expression>\n",
            "<term>\n",
            "<integerConstant> 2 </integerConstant>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> , </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier> x </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "</expressionList>\n",
            "<symbol> ) </symbol>\n",
        ]
    )


def test_expression_list(
    expression_list_tokens, compiled_expression_list_tokens
) -> None:
    engine = CompilationEngine("test", expression_list_tokens)
    engine.compile_expression_list()
    assert engine._compiled_tokens == compiled_expression_list_tokens


@fixture
def statements() -> list[str]:
    return [
        "<keyword> let </keyword>\n",
        "<identifier> game </identifier>\n",
        "<symbol> = </symbol>\n",
        "<identifier> game </identifier>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> do </keyword>\n",
        "<identifier> game </identifier>\n",
        "<symbol> . </symbol>\n",
        "<identifier> run </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> do </keyword>\n",
        "<identifier> game </identifier>\n",
        "<symbol> . </symbol>\n",
        "<identifier> dispose </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> return </keyword>\n",
        "<symbol> ; </symbol>\n",
        "<symbol> } </symbol>\n",
    ]


@fixture
def compiled_statements():
    return deque(
        [
            "<statements>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier> game </identifier>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier> game </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "<doStatement>\n",
            "<keyword> do </keyword>\n",
            "<identifier> game </identifier>\n",
            "<symbol> . </symbol>\n",
            "<identifier> run </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<expressionList>\n",
            "</expressionList>\n",
            "<symbol> ) </symbol>\n",
            "<symbol> ; </symbol>\n",
            "</doStatement>\n",
            "<doStatement>\n",
            "<keyword> do </keyword>\n",
            "<identifier> game </identifier>\n",
            "<symbol> . </symbol>\n",
            "<identifier> dispose </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<expressionList>\n",
            "</expressionList>\n",
            "<symbol> ) </symbol>\n",
            "<symbol> ; </symbol>\n",
            "</doStatement>\n",
            "<returnStatement>\n",
            "<keyword> return </keyword>\n",
            "<symbol> ; </symbol>\n",
            "</returnStatement>\n",
            "</statements>\n",
        ]
    )

def test_compile_statements(statements, compiled_statements) -> None:
    engine = CompilationEngine("test", tokens=statements)
    engine.compile_statements()
    assert engine._compiled_tokens == compiled_statements

