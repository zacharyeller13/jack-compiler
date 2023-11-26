"""Tests for tokenizer module
"""

from __future__ import annotations

from tokenizer import tokenize, deque


def test_tokenize_empty() -> None:
    empty_stack = deque()
    assert tokenize(empty_stack) == empty_stack


def test_tokenize_simple() -> None:
    stack = deque(["var int i;", "let i = 0;"])
    expected_stack = deque(["var", "int", "i", ";", "let", "i", "=", "0", ";"])
    assert tokenize(stack) == expected_stack


def test_tokenize_no_symbols() -> None:
    stack = deque(["return"])
    expected_stack = deque(["return"])
    assert tokenize(stack) == expected_stack


def test_tokenize_complex() -> None:
    stack = deque(["arg[0] = arg[1];"])
    expected_stack = deque(["arg", "[", "0", "]", "=", "arg", "[", "1", "]", ";"])
    assert tokenize(stack) == expected_stack
