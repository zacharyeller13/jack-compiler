"""
Constants for the Jack Grammar, such as comment and line-ending signifiers
"""

COMMENT = "//"
ML_COMMENT_START = "/*"
ML_COMMENT_END = "*/"
EO_TOKEN_FILE = "</tokens>"
TOKEN_TEMPLATE = "<{token_type}> {token} </{token_type}>\n"

KEYWORDS = {
    "class",
    "method",
    "function",
    "constructor",
    "int",
    "boolean",
    "char",
    "void",
    "var",
    "static",
    "field",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return",
    "true",
    "false",
    "null",
    "this",
}

SYMBOLS = {
    "{",
    "}",
    "(",
    ")",
    "[",
    "]",
    ".",
    ",",
    ";",
    "+",
    "-",
    "*",
    "/",
    "&",
    "|",
    "<",
    ">",
    "=",
    "~",
}
