"""
Tests for Compilation Engine
"""

from __future__ import annotations
from collections import deque
from pytest import fixture

from compilation_engine import CompilationEngine, is_op
from constants import VAR_DEC_START, VAR_DEC_END, TERM_START, TERM_END


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
def engine(tokens) -> CompilationEngine:
    return CompilationEngine("test", tokens)


def test_constructor(tokens, engine) -> None:
    assert isinstance(engine, CompilationEngine)
    assert engine._tokens == deque(tokens[1:])
    assert engine._filename == "test"


def test_constructor_no_tokens(tokens) -> None:
    engine = CompilationEngine("test", tokens=None, parse_func=lambda x: deque(tokens))
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


# Currently fails, b/c not fulling implemented
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
