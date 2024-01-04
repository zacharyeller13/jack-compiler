"""
Tests for tokenizer module
"""

from __future__ import annotations

from tokenizer import tokenize, deque, classify_token, escape_token


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


def test_tokenize_identifiers_next_to_symbol() -> None:
    stack = deque(["while (i < length) {"])
    expected_stack = deque(["while", "(", "i", "<", "length", ")", "{"])
    assert tokenize(stack) == expected_stack


def test_escape_tokens() -> None:
    # Not testing for '"' > "&quot;" because we should never have a standalone quotation mark
    # And string literals have the quotation mark removed when they are processed
    tokens = {"&", "<", ">", '"A string literal"'}
    expected_output = {"&amp;", "&lt;", "&gt;", "A string literal"}
    assert set(map(escape_token, tokens)) == expected_output


def test_classify_token_keyword() -> None:
    assert classify_token("if") == "keyword"


def test_classify_token_symbol() -> None:
    assert classify_token("/") == "symbol"


def test_classify_token_integer_constant() -> None:
    assert classify_token("1") == "integerConstant"


def test_classify_token_string_constant() -> None:
    assert classify_token('"a string constant"') == "stringConstant"


def test_classify_token_identifier() -> None:
    assert classify_token("x") == "identifier"
