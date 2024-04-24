"""
Constants for the Jack Grammar, such as comment and line-ending signifiers
"""

COMMENT = "//"
ML_COMMENT_START = "/*"
ML_COMMENT_END = "*/"
EO_TOKEN_FILE = "</tokens>"
TOKEN_TEMPLATE = "<{token_type}> {token} </{token_type}>\n"
VAR_DEC_START = "<varDec>\n"
VAR_DEC_END = "</varDec>\n"
STATEMENT_TERMINATOR = "<symbol> ; </symbol>\n"
LET_START = "<letStatement>\n"
LET_END = "</letStatement>\n"
TERM_START = "<term>\n"
TERM_END = "</term>\n"
EXPRESSION_START = "<expression>\n"
EXPRESSION_END = "</expression>\n"
RETURN_START = "<returnStatement>\n"
RETURN_END = "</returnStatement>\n"
DO_START = "<doStatement>\n"
DO_END = "</doStatement>\n"
OPEN_PAREN = "<symbol> ( </symbol>\n"
CLOSE_PAREN = "<symbol> ) </symbol>\n"
OPEN_BRACE = "<symbol> { </symbol>\n"
CLOSE_BRACE = "<symbol> } </symbol>\n"
MEMBER_ACCESSOR = "<symbol> . </symbol>\n"
EXPRESSION_LIST_START = "<expressionList>\n"
EXPRESSION_LIST_END = "</expressionList>\n"
IF_STATEMENT = "<ifStatement>\n"
END_IF = "</ifStatement>\n"
WHILE_START = "<whileStatement>\n"
WHILE_END = "</whileStatement>\n"

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

OPS = {
    "+",
    "-",
    "*",
    "/",
    "&",
    "|",
    "<",
    ">",
    "=",
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
    "~",
    *OPS,
}
