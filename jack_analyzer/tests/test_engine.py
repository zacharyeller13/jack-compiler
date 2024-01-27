"""
Tests for Compilation Engine
"""

from __future__ import annotations
from collections import deque
from pytest import fixture

from compilation_engine import CompilationEngine
from constants import VAR_DEC_START, VAR_DEC_END


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
