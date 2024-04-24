"""
Module and class to define the SymbolTable for interacting with and categorizing
different identifiers
"""

from __future__ import annotations
from dataclasses import dataclass, field


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

    class_table: dict[str, Identifier] = field(default_factory=dict)
    subroutine_table: dict[str, Identifier] = field(default_factory=dict)
    static_idx: int = 0
    field_idx: int = 0
    arg_idx: int = 0
    var_idx: int = 0

    def start_subroutine(self) -> None:
        """Clears the subroutine symbol table"""

        self.subroutine_table.clear()


@dataclass
class Identifier:
    """Dataclass representing a specific row of the `SymbolTable`

    Attributes:
        `name` (str): The name of the identifier
        `data_type` (str): One of 'int', 'bool', 'char', `String`, `Array`, or
            some className defined in the current .jack files
        `category` (str): One of 'var','argument','static','field','class','subroutine'
        `index` (int): The current index based on which symbol table and category
    """

    name: str
    data_type: str
    category: str
    index: int
