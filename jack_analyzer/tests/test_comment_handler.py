"""Tests for functions that remove comments
"""

from __future__ import annotations

from comment_handler import (
    is_single_comment,
    is_full_ml_comment,
    handle_complex_comments,
    remove_comments,
    deque,
)


def test_is_single_comment_returns_true() -> None:
    test_single_comment = "// This whole line is a comment"

    assert is_single_comment(test_single_comment)


def test_is_single_comment_returns_false() -> None:
    test_single_comment = "var int i; // later comment but not whole line"

    assert not is_single_comment(test_single_comment)


def test_is_full_ml_comment_returns_true() -> None:
    test_ml_comment = "/* Full line is a comment */"

    assert is_full_ml_comment(test_ml_comment)


def test_is_full_ml_comment_returns_false() -> None:
    test_ml_comment = "var int i; /* Line has a comment but not the whole thing */"

    assert not is_full_ml_comment(test_ml_comment)


def test_handle_complex_comments_single_comment() -> None:
    test_single_comment = "var int i; // later comment but not whole line"
    expected_out_line = "var int i;"

    assert handle_complex_comments(test_single_comment, False) == (
        expected_out_line,
        False,
    )


def test_handle_complex_comments_ml_comment_open() -> None:
    test_ml_comment = "/* ML comment spans multiple lines"
    expected_out_line = ""

    assert handle_complex_comments(test_ml_comment, False) == (
        expected_out_line,
        True,
    )


def test_handle_complex_comments_ml_comment_open_with_code() -> None:
    test_ml_comment = "var int i; /* ML comment spans multiple lines"
    expected_out_line = "var int i;"

    assert handle_complex_comments(test_ml_comment, False) == (
        expected_out_line,
        True,
    )


def test_handle_complex_comments_ml_comment_closed() -> None:
    test_ml_comment = "var int i; /* ML comment spans one line */"
    expected_out_line = "var int i;"

    assert handle_complex_comments(test_ml_comment, False) == (
        expected_out_line,
        False,
    )


def test_handle_complex_comments_multiple_comments_open() -> None:
    test_ml_comment = (
        "var int i; /* ML comment spans one line */ /* ML comment spans multiple lines "
    )
    expected_out_line = "var int i;"

    assert handle_complex_comments(test_ml_comment, False) == (
        expected_out_line,
        True,
    )


def test_handle_complex_comments_multiple_comments_closed() -> None:
    test_ml_comment = "/* ML comment spans one line */ var int i; /* ML comment also spans one line */"
    expected_out_line = "var int i;"

    assert handle_complex_comments(test_ml_comment, False) == (
        expected_out_line,
        False,
    )


def test_handle_complex_comments_ml_comment_already_active() -> None:
    test_ml_comment = "* This is the end of a multi-line comment */"
    expected_out_line = ""

    assert handle_complex_comments(test_ml_comment, True) == (
        expected_out_line,
        False,
    )


def test_handle_complex_comments_ml_comment_already_active_with_code() -> None:
    test_ml_comment = "* This is the end of a multi-line comment */ var int i;"
    expected_out_line = "var int i;"

    assert handle_complex_comments(test_ml_comment, True) == (
        expected_out_line,
        False,
    )


def test_handle_complex_comments_multi_comments_already_active_with_code() -> None:
    test_ml_comment = "* This is the end of a multi-line comment */ var int i; /* New multi-line comment"
    expected_out_line = "var int i;"

    assert handle_complex_comments(test_ml_comment, True) == (
        expected_out_line,
        True,
    )


def test_handle_complex_comments_multi_comments_already_active_with_code_closed() -> (
    None
):
    test_ml_comment = "* This is the end of a multi-line comment */ var int i; /* New multi-line comment */"
    expected_out_line = "var int i;"

    assert handle_complex_comments(test_ml_comment, True) == (
        expected_out_line,
        False,
    )


def test_remove_comments() -> None:
    test_contents = [
        "//This is a single line comment",
        "var int i;",
        "/* ML comment start",
        "let i = 1;",
        "ML comment end */",
        "/* Comment */ let i = 0; /* Also comment */",
    ]
    expected_output = deque(("var int i;", "let i = 0;"))

    assert remove_comments(test_contents) == expected_output
