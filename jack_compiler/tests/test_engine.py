"""
Tests for Compilation Engine
"""

from __future__ import annotations
from collections import deque
from pytest import fixture

from jack_compiler.compilation_engine import CompilationEngine, is_op
from jack_compiler.constants import (
    EXPRESSION_END,
    EXPRESSION_START,
    LET_END,
    LET_START,
    STATEMENT_TERMINATOR,
    VAR_DEC_START,
    VAR_DEC_END,
    TERM_START,
    TERM_END,
)


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
            "<identifier category='var' index=0 usage='declared'> i </identifier>\n",
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
            "<identifier category='var' index=0 usage='declared'> i </identifier>\n",
            "<symbol> , </symbol>\n",
            "<identifier category='var' index=1 usage='declared'> j </identifier>\n",
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
def let_statement_array_accessor():
    # let arr[i] = 1;
    return [
        "<keyword> let </keyword>\n",
        "<identifier> arr </identifier>\n",
        "<symbol> [ </symbol>\n",
        "<identifier> i </identifier>\n",
        "<symbol> ] </symbol>\n",
        "<symbol> = </symbol>\n",
        "<integerConstant> 1 </integerConstant>\n",
        STATEMENT_TERMINATOR,
    ]


@fixture
def compiled_let_statement_array_accessor():
    # let arr[i] = 1;
    return deque(
        [
            LET_START,
            "<keyword> let </keyword>\n",
            "<identifier category='var' index=1 usage='used'> arr </identifier>\n",
            "<symbol> [ </symbol>\n",
            EXPRESSION_START,
            TERM_START,
            "<identifier category='var' index=0 usage='used'> i </identifier>\n",
            TERM_END,
            EXPRESSION_END,
            "<symbol> ] </symbol>\n",
            "<symbol> = </symbol>\n",
            EXPRESSION_START,
            TERM_START,
            "<integerConstant> 1 </integerConstant>\n",
            TERM_END,
            EXPRESSION_END,
            STATEMENT_TERMINATOR,
            LET_END,
        ]
    )


@fixture
def engine(tokens) -> CompilationEngine:
    return CompilationEngine("test.jack", tokens=tokens)


@fixture
def test_return_statement():
    return ["<keyword> return </keyword>\n", "<symbol> ; </symbol>\n"]


def test_constructor(tokens, engine) -> None:
    assert isinstance(engine, CompilationEngine)
    assert engine._tokens == deque(tokens[1:])
    assert engine._current_filename == "test.jack"


def test_constructor_no_tokens(tokens) -> None:
    engine = CompilationEngine(
        "test.jack", tokens=None, parse_func=lambda _: deque(tokens)
    )
    assert isinstance(engine, CompilationEngine)
    assert engine._tokens == deque(tokens[1:])
    assert engine._current_filename == "test.jack"


def test_advance_token(tokens, engine) -> None:
    assert engine._current_token == tokens[0] == "<keyword> var </keyword>\n"
    engine.advance_token()
    assert engine._current_token == tokens[1] == "<keyword> int </keyword>\n"


def test_compile_var_dec(tokens, compiled_var_dec) -> None:
    engine = CompilationEngine("test.jack", tokens=tokens)
    print(engine._symbol_table)
    engine.compile_var_dec()
    assert engine._compiled_tokens == compiled_var_dec


def test_compile_var_dec_long(var_dec_long, compiled_var_dec_long) -> None:
    engine = CompilationEngine("test.jack", tokens=var_dec_long)
    engine.compile_var_dec()
    assert engine._compiled_tokens == compiled_var_dec_long


def test_expression(expression_tokens, compiled_expression) -> None:
    engine = CompilationEngine("test.jack", tokens=expression_tokens)
    engine.compile_expression()
    assert engine._compiled_tokens == compiled_expression


def test_is_op() -> None:
    assert is_op("<symbol> + </symbol>\n")


def test_term_non_identifier(term_non_identifier, compiled_term_non_identifier) -> None:
    engine = CompilationEngine("test.jack", tokens=term_non_identifier)
    engine.compile_term()
    assert engine._compiled_tokens == compiled_term_non_identifier


@fixture
def term_unary_op():
    return [
        "<symbol> ~ </symbol>\n",
        "<identifier> a </identifier>\n",
    ]


@fixture
def compiled_term_unary_op():
    return deque(
        [
            "<term>\n",
            "<symbol> ~ </symbol>\n",
            "<term>\n",
            "<identifier category='var' index=0 usage='used'> a </identifier>\n",
            "</term>\n",
            "</term>\n",
        ]
    )


def test_term_unary_op(term_unary_op, compiled_term_unary_op) -> None:
    engine = CompilationEngine("test.jack", tokens=term_unary_op)
    engine._symbol_table.define("a", "bool", "var")
    engine.compile_term()
    assert engine._compiled_tokens == compiled_term_unary_op


def test_let_statement(
    let_statement_array_accessor, compiled_let_statement_array_accessor
):
    engine = CompilationEngine("test.jack", tokens=let_statement_array_accessor)
    # We have to manually set the symbol table because this is a stub
    # Normally, these would already be declared and set while compiling
    engine._symbol_table.define("i", "int", "var")
    engine._symbol_table.define("arr", "Array", "var")
    engine.compile_let()
    assert engine._compiled_tokens == compiled_let_statement_array_accessor


@fixture
def expression_list_tokens() -> list[str]:
    return [
        "<integerConstant> 2 </integerConstant>\n",
        "<symbol> , </symbol>\n",
        "<identifier> x </identifier>\n",
        "<symbol> ) </symbol>\n",
        # This close paren is necessary, b/c we would never have expression
        # list in a vaccuum w/out parenthesis.
    ]


@fixture
def compiled_expression_list_tokens() -> deque[str]:
    return deque(
        [
            "<expressionList>\n",
            "<expression>\n",
            "<term>\n",
            "<integerConstant> 2 </integerConstant>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> , </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='var' index=0 usage='used'> x </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "</expressionList>\n",
        ]
    )


def test_expression_list(
    expression_list_tokens, compiled_expression_list_tokens
) -> None:
    engine = CompilationEngine("test.jack", tokens=expression_list_tokens)
    engine._symbol_table.define("x", "int", "var")
    engine.compile_expression_list()
    assert engine._compiled_tokens == compiled_expression_list_tokens


@fixture
def statements() -> list[str]:
    return [
        "<keyword> let </keyword>\n",
        "<identifier> game </identifier>\n",
        "<symbol> = </symbol>\n",
        "<identifier> game </identifier>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> do </keyword>\n",
        "<identifier> game </identifier>\n",
        "<symbol> . </symbol>\n",
        "<identifier> run </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> do </keyword>\n",
        "<identifier> game </identifier>\n",
        "<symbol> . </symbol>\n",
        "<identifier> dispose </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> return </keyword>\n",
        "<symbol> ; </symbol>\n",
        "<symbol> } </symbol>\n",
    ]


@fixture
def compiled_statements():
    return deque(
        [
            "<statements>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier category='var' index=0 usage='used'> game </identifier>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='var' index=0 usage='used'> game </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "<doStatement>\n",
            "<keyword> do </keyword>\n",
            "<identifier category='var' index=0 usage='used'> game </identifier>\n",
            "<symbol> . </symbol>\n",
            "<identifier category='subroutine'> run </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<expressionList>\n",
            "</expressionList>\n",
            "<symbol> ) </symbol>\n",
            "<symbol> ; </symbol>\n",
            "</doStatement>\n",
            "<doStatement>\n",
            "<keyword> do </keyword>\n",
            "<identifier category='var' index=0 usage='used'> game </identifier>\n",
            "<symbol> . </symbol>\n",
            "<identifier category='subroutine'> dispose </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<expressionList>\n",
            "</expressionList>\n",
            "<symbol> ) </symbol>\n",
            "<symbol> ; </symbol>\n",
            "</doStatement>\n",
            "<returnStatement>\n",
            "<keyword> return </keyword>\n",
            "<symbol> ; </symbol>\n",
            "</returnStatement>\n",
            "</statements>\n",
        ]
    )


def test_compile_statements(statements, compiled_statements) -> None:
    engine = CompilationEngine("test.jack", tokens=statements)
    engine._symbol_table.define("game", "Game", "var")
    engine.compile_statements()
    assert engine._compiled_tokens == compiled_statements


@fixture
def if_statement() -> list[str]:
    return [
        "<keyword> if </keyword>\n",
        "<symbol> ( </symbol>\n",
        "<identifier> b </identifier>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> { </symbol>\n",
        "<symbol> } </symbol>\n",
        "<keyword> else </keyword>\n",
        "<symbol> { </symbol>\n",
        "<symbol> } </symbol>\n",
    ]


@fixture
def compiled_if_statement() -> deque[str]:
    return deque(
        [
            "<ifStatement>\n",
            "<keyword> if </keyword>\n",
            "<symbol> ( </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='var' index=0 usage='used'> b </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ) </symbol>\n",
            "<symbol> { </symbol>\n",
            "<statements>\n",
            "</statements>\n",
            "<symbol> } </symbol>\n",
            "<keyword> else </keyword>\n",
            "<symbol> { </symbol>\n",
            "<statements>\n",
            "</statements>\n",
            "<symbol> } </symbol>\n",
            "</ifStatement>\n",
        ]
    )


def test_if_statement(if_statement, compiled_if_statement) -> None:
    engine = CompilationEngine("test.jack", tokens=if_statement)
    engine._symbol_table.define("b", "bool", "var")
    engine.compile_if()
    assert engine._compiled_tokens == compiled_if_statement


@fixture
def while_statement() -> list[str]:
    return [
        "<keyword> while </keyword>\n",
        "<symbol> ( </symbol>\n",
        "<identifier> i </identifier>\n",
        "<symbol> &lt; </symbol>\n",
        "<identifier> length </identifier>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> { </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> a </identifier>\n",
        "<symbol> [ </symbol>\n",
        "<identifier> i </identifier>\n",
        "<symbol> ] </symbol>\n",
        "<symbol> = </symbol>\n",
        "<identifier> Keyboard </identifier>\n",
        "<symbol> . </symbol>\n",
        "<identifier> readInt </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<stringConstant> ENTER THE NEXT NUMBER:  </stringConstant>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> i </identifier>\n",
        "<symbol> = </symbol>\n",
        "<identifier> i </identifier>\n",
        "<symbol> + </symbol>\n",
        "<integerConstant> 1 </integerConstant>\n",
        "<symbol> ; </symbol>\n",
        "<symbol> } </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> i </identifier>\n",
        "<symbol> = </symbol>\n",
        "<integerConstant> 0 </integerConstant>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> sum </identifier>\n",
        "<symbol> = </symbol>\n",
        "<integerConstant> 0 </integerConstant>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> while </keyword>\n",
        "<symbol> ( </symbol>\n",
        "<identifier> i </identifier>\n",
        "<symbol> &lt; </symbol>\n",
        "<identifier> length </identifier>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> { </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> sum </identifier>\n",
        "<symbol> = </symbol>\n",
        "<identifier> sum </identifier>\n",
        "<symbol> + </symbol>\n",
        "<identifier> a </identifier>\n",
        "<symbol> [ </symbol>\n",
        "<identifier> i </identifier>\n",
        "<symbol> ] </symbol>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> i </identifier>\n",
        "<symbol> = </symbol>\n",
        "<identifier> i </identifier>\n",
        "<symbol> + </symbol>\n",
        "<integerConstant> 1 </integerConstant>\n",
        "<symbol> ; </symbol>\n",
        "<symbol> } </symbol>\n",
    ]


@fixture
def compiled_while_statement() -> deque[str]:
    return deque(
        [
            "<whileStatement>\n",
            "<keyword> while </keyword>\n",
            "<symbol> ( </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='var' index=1 usage='used'> i </identifier>\n",
            "</term>\n",
            "<symbol> &lt; </symbol>\n",
            "<term>\n",
            "<identifier category='var' index=0 usage='used'> length </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ) </symbol>\n",
            "<symbol> { </symbol>\n",
            "<statements>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier category='var' index=2 usage='used'> a </identifier>\n",
            "<symbol> [ </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='var' index=1 usage='used'> i </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ] </symbol>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='class'> Keyboard </identifier>\n",
            "<symbol> . </symbol>\n",
            "<identifier category='subroutine'> readInt </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<expressionList>\n",
            "<expression>\n",
            "<term>\n",
            "<stringConstant> ENTER THE NEXT NUMBER:  </stringConstant>\n",
            "</term>\n",
            "</expression>\n",
            "</expressionList>\n",
            "<symbol> ) </symbol>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier category='var' index=1 usage='used'> i </identifier>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='var' index=1 usage='used'> i </identifier>\n",
            "</term>\n",
            "<symbol> + </symbol>\n",
            "<term>\n",
            "<integerConstant> 1 </integerConstant>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "</statements>\n",
            "<symbol> } </symbol>\n",
            "</whileStatement>\n",
        ]
    )


def test_while_statement(while_statement, compiled_while_statement) -> None:
    engine = CompilationEngine("test.jack", tokens=while_statement)
    engine._symbol_table.define("length", "int", "var")
    engine._symbol_table.define("i", "int", "var")
    engine._symbol_table.define("a", "Array", "var")
    engine.compile_while()
    assert engine._compiled_tokens == compiled_while_statement


@fixture
def subroutine_call() -> list[str]:
    return [
        "<identifier> Keyboard </identifier>\n",
        "<symbol> . </symbol>\n",
        "<identifier> readInt </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<stringConstant> ENTER THE NEXT NUMBER:  </stringConstant>\n",
        "<symbol> ) </symbol>\n",
    ]


@fixture
def compiled_subroutine_call() -> deque[str]:
    return deque(
        [
            "<expression>\n",
            "<term>\n",
            "<identifier category='class'> Keyboard </identifier>\n",
            "<symbol> . </symbol>\n",
            "<identifier category='subroutine'> readInt </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<expressionList>\n",
            "<expression>\n",
            "<term>\n",
            "<stringConstant> ENTER THE NEXT NUMBER:  </stringConstant>\n",
            "</term>\n",
            "</expression>\n",
            "</expressionList>\n",
            "<symbol> ) </symbol>\n",
            "</term>\n",
            "</expression>\n",
        ]
    )


def test_subroutine_call(subroutine_call, compiled_subroutine_call) -> None:
    engine = CompilationEngine("test.jack", tokens=subroutine_call)
    engine.compile_expression()
    assert engine._compiled_tokens == compiled_subroutine_call


@fixture
def subroutine_body() -> list[str]:
    return [
        "<symbol> { </symbol>\n",
        "<keyword> var </keyword>\n",
        "<identifier> Array </identifier>\n",
        "<identifier> a </identifier>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> var </keyword>\n",
        "<keyword> int </keyword>\n",
        "<identifier> length </identifier>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> var </keyword>\n",
        "<keyword> int </keyword>\n",
        "<identifier> i </identifier>\n",
        "<symbol> , </symbol>\n",
        "<identifier> sum </identifier>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> length </identifier>\n",
        "<symbol> = </symbol>\n",
        "<identifier> Keyboard </identifier>\n",
        "<symbol> . </symbol>\n",
        "<identifier> readInt </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<stringConstant> HOW MANY NUMBERS?  </stringConstant>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> a </identifier>\n",
        "<symbol> = </symbol>\n",
        "<identifier> Array </identifier>\n",
        "<symbol> . </symbol>\n",
        "<identifier> new </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<identifier> length </identifier>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> i </identifier>\n",
        "<symbol> = </symbol>\n",
        "<integerConstant> 0 </integerConstant>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> while </keyword>\n",
        "<symbol> ( </symbol>\n",
        "<identifier> i </identifier>\n",
        "<symbol> &lt; </symbol>\n",
        "<identifier> length </identifier>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> { </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> a </identifier>\n",
        "<symbol> [ </symbol>\n",
        "<identifier> i </identifier>\n",
        "<symbol> ] </symbol>\n",
        "<symbol> = </symbol>\n",
        "<identifier> Keyboard </identifier>\n",
        "<symbol> . </symbol>\n",
        "<identifier> readInt </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<stringConstant> ENTER THE NEXT NUMBER:  </stringConstant>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> i </identifier>\n",
        "<symbol> = </symbol>\n",
        "<identifier> i </identifier>\n",
        "<symbol> + </symbol>\n",
        "<integerConstant> 1 </integerConstant>\n",
        "<symbol> ; </symbol>\n",
        "<symbol> } </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> i </identifier>\n",
        "<symbol> = </symbol>\n",
        "<integerConstant> 0 </integerConstant>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> sum </identifier>\n",
        "<symbol> = </symbol>\n",
        "<integerConstant> 0 </integerConstant>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> while </keyword>\n",
        "<symbol> ( </symbol>\n",
        "<identifier> i </identifier>\n",
        "<symbol> &lt; </symbol>\n",
        "<identifier> length </identifier>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> { </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> sum </identifier>\n",
        "<symbol> = </symbol>\n",
        "<identifier> sum </identifier>\n",
        "<symbol> + </symbol>\n",
        "<identifier> a </identifier>\n",
        "<symbol> [ </symbol>\n",
        "<identifier> i </identifier>\n",
        "<symbol> ] </symbol>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> i </identifier>\n",
        "<symbol> = </symbol>\n",
        "<identifier> i </identifier>\n",
        "<symbol> + </symbol>\n",
        "<integerConstant> 1 </integerConstant>\n",
        "<symbol> ; </symbol>\n",
        "<symbol> } </symbol>\n",
        "<keyword> do </keyword>\n",
        "<identifier> Output </identifier>\n",
        "<symbol> . </symbol>\n",
        "<identifier> printString </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<stringConstant> THE AVERAGE IS:  </stringConstant>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> do </keyword>\n",
        "<identifier> Output </identifier>\n",
        "<symbol> . </symbol>\n",
        "<identifier> printInt </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<identifier> sum </identifier>\n",
        "<symbol> / </symbol>\n",
        "<identifier> length </identifier>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> do </keyword>\n",
        "<identifier> Output </identifier>\n",
        "<symbol> . </symbol>\n",
        "<identifier> println </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> return </keyword>\n",
        "<symbol> ; </symbol>\n",
        "<symbol> } </symbol>\n",
        "<symbol> } </symbol>\n",
    ]


@fixture
def compiled_subroutine_body() -> deque[str]:
    return deque(
        [
            "<subroutineBody>\n",
            "<symbol> { </symbol>\n",
            "<varDec>\n",
            "<keyword> var </keyword>\n",
            "<identifier category='class'> Array </identifier>\n",
            "<identifier category='var' index=0 usage='declared'> a </identifier>\n",
            "<symbol> ; </symbol>\n",
            "</varDec>\n",
            "<varDec>\n",
            "<keyword> var </keyword>\n",
            "<keyword> int </keyword>\n",
            "<identifier category='var' index=1 usage='declared'> length </identifier>\n",
            "<symbol> ; </symbol>\n",
            "</varDec>\n",
            "<varDec>\n",
            "<keyword> var </keyword>\n",
            "<keyword> int </keyword>\n",
            "<identifier category='var' index=2 usage='declared'> i </identifier>\n",
            "<symbol> , </symbol>\n",
            "<identifier category='var' index=3 usage='declared'> sum </identifier>\n",
            "<symbol> ; </symbol>\n",
            "</varDec>\n",
            "<statements>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier category='var' index=1 usage='used'> length </identifier>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='class'> Keyboard </identifier>\n",
            "<symbol> . </symbol>\n",
            "<identifier category='subroutine'> readInt </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<expressionList>\n",
            "<expression>\n",
            "<term>\n",
            "<stringConstant> HOW MANY NUMBERS?  </stringConstant>\n",
            "</term>\n",
            "</expression>\n",
            "</expressionList>\n",
            "<symbol> ) </symbol>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier category='var' index=0 usage='used'> a </identifier>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='class'> Array </identifier>\n",
            "<symbol> . </symbol>\n",
            "<identifier category='subroutine'> new </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<expressionList>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='var' index=1 usage='used'> length </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "</expressionList>\n",
            "<symbol> ) </symbol>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier category='var' index=2 usage='used'> i </identifier>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<integerConstant> 0 </integerConstant>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "<whileStatement>\n",
            "<keyword> while </keyword>\n",
            "<symbol> ( </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='var' index=2 usage='used'> i </identifier>\n",
            "</term>\n",
            "<symbol> &lt; </symbol>\n",
            "<term>\n",
            "<identifier category='var' index=1 usage='used'> length </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ) </symbol>\n",
            "<symbol> { </symbol>\n",
            "<statements>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier category='var' index=0 usage='used'> a </identifier>\n",
            "<symbol> [ </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='var' index=2 usage='used'> i </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ] </symbol>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='class'> Keyboard </identifier>\n",
            "<symbol> . </symbol>\n",
            "<identifier category='subroutine'> readInt </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<expressionList>\n",
            "<expression>\n",
            "<term>\n",
            "<stringConstant> ENTER THE NEXT NUMBER:  </stringConstant>\n",
            "</term>\n",
            "</expression>\n",
            "</expressionList>\n",
            "<symbol> ) </symbol>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier category='var' index=2 usage='used'> i </identifier>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='var' index=2 usage='used'> i </identifier>\n",
            "</term>\n",
            "<symbol> + </symbol>\n",
            "<term>\n",
            "<integerConstant> 1 </integerConstant>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "</statements>\n",
            "<symbol> } </symbol>\n",
            "</whileStatement>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier category='var' index=2 usage='used'> i </identifier>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<integerConstant> 0 </integerConstant>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier category='var' index=3 usage='used'> sum </identifier>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<integerConstant> 0 </integerConstant>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "<whileStatement>\n",
            "<keyword> while </keyword>\n",
            "<symbol> ( </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='var' index=2 usage='used'> i </identifier>\n",
            "</term>\n",
            "<symbol> &lt; </symbol>\n",
            "<term>\n",
            "<identifier category='var' index=1 usage='used'> length </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ) </symbol>\n",
            "<symbol> { </symbol>\n",
            "<statements>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier category='var' index=3 usage='used'> sum </identifier>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='var' index=3 usage='used'> sum </identifier>\n",
            "</term>\n",
            "<symbol> + </symbol>\n",
            "<term>\n",
            "<identifier category='var' index=0 usage='used'> a </identifier>\n",
            "<symbol> [ </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='var' index=2 usage='used'> i </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ] </symbol>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier category='var' index=2 usage='used'> i </identifier>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='var' index=2 usage='used'> i </identifier>\n",
            "</term>\n",
            "<symbol> + </symbol>\n",
            "<term>\n",
            "<integerConstant> 1 </integerConstant>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "</statements>\n",
            "<symbol> } </symbol>\n",
            "</whileStatement>\n",
            "<doStatement>\n",
            "<keyword> do </keyword>\n",
            "<identifier category='class'> Output </identifier>\n",
            "<symbol> . </symbol>\n",
            "<identifier category='subroutine'> printString </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<expressionList>\n",
            "<expression>\n",
            "<term>\n",
            "<stringConstant> THE AVERAGE IS:  </stringConstant>\n",
            "</term>\n",
            "</expression>\n",
            "</expressionList>\n",
            "<symbol> ) </symbol>\n",
            "<symbol> ; </symbol>\n",
            "</doStatement>\n",
            "<doStatement>\n",
            "<keyword> do </keyword>\n",
            "<identifier category='class'> Output </identifier>\n",
            "<symbol> . </symbol>\n",
            "<identifier category='subroutine'> printInt </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<expressionList>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='var' index=3 usage='used'> sum </identifier>\n",
            "</term>\n",
            "<symbol> / </symbol>\n",
            "<term>\n",
            "<identifier category='var' index=1 usage='used'> length </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "</expressionList>\n",
            "<symbol> ) </symbol>\n",
            "<symbol> ; </symbol>\n",
            "</doStatement>\n",
            "<doStatement>\n",
            "<keyword> do </keyword>\n",
            "<identifier category='class'> Output </identifier>\n",
            "<symbol> . </symbol>\n",
            "<identifier category='subroutine'> println </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<expressionList>\n",
            "</expressionList>\n",
            "<symbol> ) </symbol>\n",
            "<symbol> ; </symbol>\n",
            "</doStatement>\n",
            "<returnStatement>\n",
            "<keyword> return </keyword>\n",
            "<symbol> ; </symbol>\n",
            "</returnStatement>\n",
            "</statements>\n",
            "<symbol> } </symbol>\n",
            "</subroutineBody>\n",
        ]
    )


def test_subroutine_body(subroutine_body, compiled_subroutine_body) -> None:
    engine = CompilationEngine("test.jack", tokens=subroutine_body)
    engine.compile_subroutine_body()
    assert engine._compiled_tokens == compiled_subroutine_body


@fixture
def class_var_dec() -> list[str]:
    return [
        "<keyword> field </keyword>\n",
        "<keyword> int </keyword>\n",
        "<identifier> x </identifier>\n",
        "<symbol> , </symbol>\n",
        "<identifier> y </identifier>\n",
        "<symbol> ; </symbol>\n",
    ]


@fixture
def compiled_class_var_dec() -> deque[str]:
    return deque(
        [
            "<classVarDec>\n",
            "<keyword> field </keyword>\n",
            "<keyword> int </keyword>\n",
            "<identifier category='field' index=0 usage='declared'> x </identifier>\n",
            "<symbol> , </symbol>\n",
            "<identifier category='field' index=1 usage='declared'> y </identifier>\n",
            "<symbol> ; </symbol>\n",
            "</classVarDec>\n",
        ]
    )


def test_class_var_dec(class_var_dec, compiled_class_var_dec) -> None:
    engine = CompilationEngine("test.jack", tokens=class_var_dec)
    engine.compile_class_var_dec()
    assert engine._compiled_tokens == compiled_class_var_dec


@fixture
def subroutine_dec_no_parameters() -> list[str]:
    return [
        "<keyword> method </keyword>\n",
        "<keyword> void </keyword>\n",
        "<identifier> dispose </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> { </symbol>\n",
        "<keyword> do </keyword>\n",
        "<identifier> Memory </identifier>\n",
        "<symbol> . </symbol>\n",
        "<identifier> deAlloc </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<keyword> this </keyword>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> return </keyword>\n",
        "<symbol> ; </symbol>\n",
        "<symbol> } </symbol>\n",
    ]


@fixture
def compiled_subroutine_dec_no_parameters() -> deque[str]:
    return deque(
        [
            "<subroutineDec>\n",
            "<keyword> method </keyword>\n",
            "<keyword> void </keyword>\n",
            "<identifier category='subroutine'> dispose </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<parameterList>\n",
            "</parameterList>\n",
            "<symbol> ) </symbol>\n",
            "<subroutineBody>\n",
            "<symbol> { </symbol>\n",
            "<statements>\n",
            "<doStatement>\n",
            "<keyword> do </keyword>\n",
            "<identifier category='class'> Memory </identifier>\n",
            "<symbol> . </symbol>\n",
            "<identifier category='subroutine'> deAlloc </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<expressionList>\n",
            "<expression>\n",
            "<term>\n",
            "<keyword> this </keyword>\n",
            "</term>\n",
            "</expression>\n",
            "</expressionList>\n",
            "<symbol> ) </symbol>\n",
            "<symbol> ; </symbol>\n",
            "</doStatement>\n",
            "<returnStatement>\n",
            "<keyword> return </keyword>\n",
            "<symbol> ; </symbol>\n",
            "</returnStatement>\n",
            "</statements>\n",
            "<symbol> } </symbol>\n",
            "</subroutineBody>\n",
            "</subroutineDec>\n",
        ]
    )


def test_subroutine_dec_no_parameters(
    subroutine_dec_no_parameters, compiled_subroutine_dec_no_parameters
) -> None:
    engine = CompilationEngine("test.jack", tokens=subroutine_dec_no_parameters)
    engine.compile_subroutine_dec()
    assert engine._compiled_tokens == compiled_subroutine_dec_no_parameters


@fixture
def subroutine_dec() -> list[str]:
    return [
        "<keyword> constructor </keyword>\n",
        "<identifier> Square </identifier>\n",
        "<identifier> new </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<keyword> int </keyword>\n",
        "<identifier> Ax </identifier>\n",
        "<symbol> , </symbol>\n",
        "<keyword> int </keyword>\n",
        "<identifier> Ay </identifier>\n",
        "<symbol> , </symbol>\n",
        "<keyword> int </keyword>\n",
        "<identifier> Asize </identifier>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> { </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> x </identifier>\n",
        "<symbol> = </symbol>\n",
        "<identifier> Ax </identifier>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> y </identifier>\n",
        "<symbol> = </symbol>\n",
        "<identifier> Ay </identifier>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> let </keyword>\n",
        "<identifier> size </identifier>\n",
        "<symbol> = </symbol>\n",
        "<identifier> Asize </identifier>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> do </keyword>\n",
        "<identifier> draw </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> ; </symbol>\n",
        "<keyword> return </keyword>\n",
        "<keyword> this </keyword>\n",
        "<symbol> ; </symbol>\n",
        "<symbol> } </symbol>\n",
    ]


@fixture
def compiled_subroutine_dec() -> deque[str]:
    return deque(
        [
            "<subroutineDec>\n",
            "<keyword> constructor </keyword>\n",
            "<identifier category='class'> Square </identifier>\n",
            "<identifier category='subroutine'> new </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<parameterList>\n",
            "<keyword> int </keyword>\n",
            "<identifier category='arg' index=0 usage='declared'> Ax </identifier>\n",
            "<symbol> , </symbol>\n",
            "<keyword> int </keyword>\n",
            "<identifier category='arg' index=1 usage='declared'> Ay </identifier>\n",
            "<symbol> , </symbol>\n",
            "<keyword> int </keyword>\n",
            "<identifier category='arg' index=2 usage='declared'> Asize </identifier>\n",
            "</parameterList>\n",
            "<symbol> ) </symbol>\n",
            "<subroutineBody>\n",
            "<symbol> { </symbol>\n",
            "<statements>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier category='field' index=0 usage='used'> x </identifier>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='arg' index=0 usage='used'> Ax </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier category='field' index=1 usage='used'> y </identifier>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='arg' index=1 usage='used'> Ay </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "<letStatement>\n",
            "<keyword> let </keyword>\n",
            "<identifier category='field' index=2 usage='used'> size </identifier>\n",
            "<symbol> = </symbol>\n",
            "<expression>\n",
            "<term>\n",
            "<identifier category='arg' index=2 usage='used'> Asize </identifier>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</letStatement>\n",
            "<doStatement>\n",
            "<keyword> do </keyword>\n",
            "<identifier category='subroutine'> draw </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<expressionList>\n",
            "</expressionList>\n",
            "<symbol> ) </symbol>\n",
            "<symbol> ; </symbol>\n",
            "</doStatement>\n",
            "<returnStatement>\n",
            "<keyword> return </keyword>\n",
            "<expression>\n",
            "<term>\n",
            "<keyword> this </keyword>\n",
            "</term>\n",
            "</expression>\n",
            "<symbol> ; </symbol>\n",
            "</returnStatement>\n",
            "</statements>\n",
            "<symbol> } </symbol>\n",
            "</subroutineBody>\n",
            "</subroutineDec>\n",
        ]
    )


def test_subroutine_dec(subroutine_dec, compiled_subroutine_dec) -> None:
    engine = CompilationEngine("test.jack", tokens=subroutine_dec)
    # 3 fields: x, y, and size
    engine._symbol_table.define("x", "int", "field")
    engine._symbol_table.define("y", "int", "field")
    engine._symbol_table.define("size", "int", "field")
    engine.compile_subroutine_dec()
    assert engine._compiled_tokens == compiled_subroutine_dec
