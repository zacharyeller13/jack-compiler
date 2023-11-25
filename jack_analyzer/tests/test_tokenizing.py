"""Tests for tokenizer module
"""

from __future__ import annotations

from tokenizer import tokenize, deque

def test_tokenize_empty() -> None:
    empty_stack = deque()
    assert tokenize(empty_stack) == deque()

def test_tokenize_simple() -> None:
    stack = deque(["var int i;", "let i = 0;"])
    assert tokenize(stack) == deque(["var", "int", "i", ";", "let", "i", "=", "0"])
