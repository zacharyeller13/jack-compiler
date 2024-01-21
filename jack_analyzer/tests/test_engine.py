"""
Tests for Compilation Engine
"""

from __future__ import annotations
from collections import deque
from pytest import fixture

from compilation_engine import CompilationEngine


@fixture
def tokens():
    yield [
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


def test_constructor(tokens) -> None:
    engine = CompilationEngine(
        "test",
        tokens=tokens,
    )
    assert isinstance(engine, CompilationEngine)
    assert engine._tokens == deque(tokens)
    assert engine._filename == "test"


def test_constructor_no_tokens(tokens) -> None:
    engine = CompilationEngine("test", tokens=None, parse_func=lambda x: deque(tokens))
    assert isinstance(engine, CompilationEngine)
    assert engine._tokens == deque(tokens)
    assert engine._filename == "test"
