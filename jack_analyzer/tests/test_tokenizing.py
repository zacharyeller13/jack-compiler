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


def test_tokenize_with_string_constants() -> None:
    stack = deque(['let stringVal = "hello world";'])
    expected_stack = deque(["let", "stringVal", "=", '"hello world"', ";"])
    assert tokenize(stack) == expected_stack


def test_tokenize_with_string_constants_containing_symbol() -> None:
    stack = deque(['let stringVal = "hello; world";'])
    expected_stack = deque(["let", "stringVal", "=", '"hello; world"', ";"])
    assert tokenize(stack) == expected_stack


def test_tokenize_empty_string_constant() -> None:
    stack = deque(['let stringVal = "";'])
    expected_stack = deque(["let", "stringVal", "=", '""', ";"])
    assert tokenize(stack) == expected_stack


def test_tokenize_string_constant_no_whitespace() -> None:
    stack = deque(['let stringVal = "a";'])
    expected_stack = deque(["let", "stringVal", "=", '"a"', ";"])
    assert tokenize(stack) == expected_stack
