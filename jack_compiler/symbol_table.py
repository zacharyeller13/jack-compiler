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
    indexes: dict[str, int] = field(
        default_factory=lambda: {"static": 0, "field": 0, "arg": 0, "var": 0}
    )

    def start_subroutine(self) -> None:
        """Clears the subroutine symbol table"""

        self.subroutine_table.clear()

    def define(self, name: str, data_type: str, category: str) -> None:
        """Defines a new identifier of given name, type, kind and assigns it
            a running index

        Args:
            `name` (str): The identifier name
            `data_type` (str): The datatype of the new Identifier. See `Identifier`
                for list of possible types
            `category` (str): The category of the new Identifier. See `Identifier`
                for list of possible types

        Raises:
            `ValueError`: If the provided identifier already exists in the table
                to which it would be assigned
        """

        # Define the new index
        new_idx = self.indexes[category]
        self.indexes[category] += 1

        # Create the new identifier
        new_id = Identifier(
            name=name, data_type=data_type, category=category, index=new_idx
        )

        # Add it to class or subroutine table depending on type
        if category in {"static", "field"}:
            if exist_id := self.class_table.get(name):
                raise ValueError(
                    f"{name} already exists in the class table. {exist_id}"
                )

            self.class_table[name] = new_id
        else:
            if exist_id := self.subroutine_table.get(name):
                raise ValueError(
                    f"{name} already exists in the subroutine table. {exist_id}"
                )

            self.subroutine_table[name] = new_id


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
