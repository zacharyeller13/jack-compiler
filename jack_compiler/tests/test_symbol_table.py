from collections import deque
from dataclasses import asdict
from pytest import fixture

from symbol_table import Identifier, SymbolTable
from compilation_engine import CompilationEngine


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
