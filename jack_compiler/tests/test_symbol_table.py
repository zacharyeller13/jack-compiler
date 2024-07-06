from collections import deque
from dataclasses import asdict
from pytest import fixture

from jack_compiler.symbol_table import Identifier, SymbolTable
from jack_compiler.compilation_engine_xml import CompilationEngine


@fixture
def test_class_var_tokens() -> list[str]:
    return [
        "<keyword> static </keyword>\n",
        "<keyword> int </keyword>\n",
        "<identifier> x </keyword>\n",
        "<symbol> ; </symbol>\n",
    ]


@fixture
def compiled_class_var_tokens() -> deque[str]:
    return deque(
        [
            "<classVarDec>\n",
            "<keyword> static </keyword>\n",
            "<keyword> int </keyword>\n",
            "<identifier category='static' index=0 usage='declared'> x </identifier>\n",
            "<symbol> ; </symbol>\n",
            "</classVarDec>\n",
        ]
    )


@fixture
def test_class_var_symbol_table():
    identifier = Identifier(name="x", data_type="int", category="static", index=0)
    table = SymbolTable(
        class_table={"x": identifier},
        indexes={"static": 1, "field": 0, "arg": 0, "var": 0},
    )
    yield table
    del table


def test_class_var_dec(test_class_var_tokens, test_class_var_symbol_table) -> None:
    engine = CompilationEngine("test", tokens=test_class_var_tokens)
    engine.compile_class_var_dec()
    assert asdict(engine._symbol_table) == asdict(test_class_var_symbol_table)


def test_base_symbol_table():
    assert SymbolTable() == SymbolTable()


def test_base_identifier():
    assert Identifier("test", "int", "static", 0) == Identifier(
        "test", "int", "static", 0
    )


def test_basic_symbol_table():
    assert SymbolTable(
        class_table={
            "x": Identifier(name="x", data_type="int", category="static", index=0)
        },
        indexes={"static": 1, "field": 0, "arg": 0, "var": 0},
    ) == SymbolTable(
        class_table={
            "x": Identifier(name="x", data_type="int", category="static", index=0)
        },
        indexes={"static": 1, "field": 0, "arg": 0, "var": 0},
    )


def test_class_var_dec_output(test_class_var_tokens, compiled_class_var_tokens) -> None:
    engine = CompilationEngine("test", tokens=test_class_var_tokens)
    engine.compile_class_var_dec()
    assert engine._compiled_tokens == compiled_class_var_tokens


@fixture
def test_multi_class_var_tokens() -> list[str]:
    return [
        "<keyword> static </keyword>\n",
        "<keyword> int </keyword>\n",
        "<identifier> x </keyword>\n",
        "<symbol> , </symbol>\n",
        "<identifier> y </keyword>\n",
        "<symbol> , </symbol>\n",
        "<identifier> z </keyword>\n",
        "<symbol> ; </symbol>\n",
    ]


@fixture
def compiled_multi_class_var_tokens() -> deque[str]:
    return deque(
        [
            "<classVarDec>\n",
            "<keyword> static </keyword>\n",
            "<keyword> int </keyword>\n",
            "<identifier category='static' index=0 usage='declared'> x </identifier>\n",
            "<symbol> , </symbol>\n",
            "<identifier category='static' index=1 usage='declared'> y </identifier>\n",
            "<symbol> , </symbol>\n",
            "<identifier category='static' index=2 usage='declared'> z </identifier>\n",
            "<symbol> ; </symbol>\n",
            "</classVarDec>\n",
        ]
    )


@fixture
def test_multi_class_var_symbol_table():
    x = Identifier(name="x", data_type="int", category="static", index=0)
    y = Identifier(name="y", data_type="int", category="static", index=1)
    z = Identifier(name="z", data_type="int", category="static", index=2)
    table = SymbolTable(
        class_table={"x": x, "y": y, "z": z},
        indexes={"static": 3, "field": 0, "arg": 0, "var": 0},
    )
    yield table
    del table


def test_multi_class_var_dec_output(
    test_multi_class_var_tokens, compiled_multi_class_var_tokens
) -> None:
    engine = CompilationEngine("test", tokens=test_multi_class_var_tokens)
    engine.compile_class_var_dec()
    assert engine._compiled_tokens == compiled_multi_class_var_tokens


@fixture
def test_subroutine_dec_tokens() -> list[str]:
    return [
        "<keyword> function </keyword>\n",
        "<keyword> void </keyword>\n",
        "<identifier> func </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> { </symbol>\n",
        "<symbol> } </symbol>\n",
    ]


@fixture
def compiled_subroutine_dec_tokens() -> deque[str]:
    return deque(
        [
            "<subroutineDec>\n",
            "<keyword> function </keyword>\n",
            "<keyword> void </keyword>\n",
            "<identifier category='subroutine'> func </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<parameterList>\n",
            "</parameterList>\n",
            "<symbol> ) </symbol>\n",
            "<subroutineBody>\n",
            "<symbol> { </symbol>\n",
            "<symbol> } </symbol>\n",
            "</subroutineBody>\n",
            "</subroutineDec>\n",
        ]
    )


def test_subroutine_dec_empty_body(
    test_subroutine_dec_tokens, compiled_subroutine_dec_tokens
) -> None:
    """Subroutine declaration should just clear the subroutine table"""
    engine = CompilationEngine("test", tokens=test_subroutine_dec_tokens)
    engine.compile_subroutine_dec()
    assert engine._compiled_tokens == compiled_subroutine_dec_tokens
    assert len(engine._symbol_table.subroutine_table) == 0


@fixture
def test_subroutine_dec_method_tokens() -> list[str]:
    return [
        "<keyword> method </keyword>\n",
        "<keyword> void </keyword>\n",
        "<identifier> func </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> { </symbol>\n",
        "<symbol> } </symbol>\n",
    ]


@fixture
def compiled_subroutine_dec_method_tokens() -> deque[str]:
    return deque(
        [
            "<subroutineDec>\n",
            "<keyword> method </keyword>\n",
            "<keyword> void </keyword>\n",
            "<identifier category='subroutine'> func </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<parameterList>\n",
            "</parameterList>\n",
            "<symbol> ) </symbol>\n",
            "<subroutineBody>\n",
            "<symbol> { </symbol>\n",
            "<symbol> } </symbol>\n",
            "</subroutineBody>\n",
            "</subroutineDec>\n",
        ]
    )


def test_subroutine_dec_method(
    test_subroutine_dec_method_tokens, compiled_subroutine_dec_method_tokens
) -> None:
    """Subroutine declaration should just clear the subroutine table"""
    engine = CompilationEngine("test", tokens=test_subroutine_dec_method_tokens)
    engine.compile_subroutine_dec()
    assert engine._compiled_tokens == compiled_subroutine_dec_method_tokens
    assert len(engine._symbol_table.subroutine_table) == 1
    assert asdict(engine._symbol_table.subroutine_table.get("this")) == asdict(
        Identifier(name="this", data_type="test", category="arg", index=0)
    )


@fixture
def test_subroutine_dec_parameter_tokens() -> list[str]:
    return [
        "<keyword> function </keyword>\n",
        "<keyword> void </keyword>\n",
        "<identifier> func </identifier>\n",
        "<symbol> ( </symbol>\n",
        "<keyword> int </keyword>\n",
        "<identifier> x </identifier>\n",
        "<symbol> ) </symbol>\n",
        "<symbol> { </symbol>\n",
        "<symbol> } </symbol>\n",
    ]


@fixture
def compiled_subroutine_dec_parameter_tokens() -> deque[str]:
    return deque(
        [
            "<subroutineDec>\n",
            "<keyword> function </keyword>\n",
            "<keyword> void </keyword>\n",
            "<identifier category='subroutine'> func </identifier>\n",
            "<symbol> ( </symbol>\n",
            "<parameterList>\n",
            "<keyword> int </keyword>\n",
            "<identifier category='arg' index=0 usage='declared'> x </identifier>\n",
            "</parameterList>\n",
            "<symbol> ) </symbol>\n",
            "<subroutineBody>\n",
            "<symbol> { </symbol>\n",
            "<symbol> } </symbol>\n",
            "</subroutineBody>\n",
            "</subroutineDec>\n",
        ]
    )


def test_subroutine_dec_parameter(
    test_subroutine_dec_parameter_tokens, compiled_subroutine_dec_parameter_tokens
) -> None:
    """Subroutine declaration should just clear the subroutine table"""
    engine = CompilationEngine("test", tokens=test_subroutine_dec_parameter_tokens)
    engine.compile_subroutine_dec()
    assert engine._compiled_tokens == compiled_subroutine_dec_parameter_tokens
    assert len(engine._symbol_table.subroutine_table) == 1
    assert asdict(engine._symbol_table.subroutine_table.get("x")) == asdict(
        Identifier(name="x", data_type="int", category="arg", index=0)
    )
