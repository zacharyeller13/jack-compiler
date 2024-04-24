"""
Module and class to define the SymbolTable for interacting with and categorizing
different identifiers
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SymbolTable:
    """Dataclass representing a symbol table holding information about each identifier
    in a given compilation scope

    Attributes:
        `class_table` (dict[str, Identifier]): A dictionary of Identifiers, key is the
            identifier name
        `subroutine_table` (dict[str, Identifier]): A dictionary of Identifiers, key is
            the Identifier name
        `static_idx` (int): Current index of all static class vars
        `field_idx` (int): Current index of all field class vars
        `arg_idx` (int): Current index of all arg subroutine vars
        `var_idx` (int): Current index of all local subroutine vars
    """

    class_table: dict[str, Identifier]
    subroutine_table: dict[str, Identifier]
    static_idx: int
    field_idx: int
    arg_idx: int
    var_idx: int


@dataclass
class Identifier:
    """Dataclass representing a specific row of the `SymbolTable`

    Attributes:
        `name` (str): The name of the identifier
        `category` (str): One of 'var','argument','static','field','class','subroutine'
        `index` (int): The current index based on which symbol table and category
    """

    name: str
    category: str
    index: int
