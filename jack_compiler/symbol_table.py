"""
Module and class to define the SymbolTable for interacting with and categorizing
different identifiers
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SymbolTable:
    """Dataclass representing a symbol table holding information about each identifier
    in a given compilation scope

    Attributes:
        `class_table` (dict[str, Identifier]): A dictionary of Identifiers, key is the
            identifier name
        `subroutine_table` (dict[str, Identifier]): A dictionary of Identifiers, key is
            the Identifier name
        `indexes` (dict[str, int]): All 4 indexes (static, field, arg, var).
    """

    class_table: dict[str, Identifier] = field(default_factory=dict)
    subroutine_table: dict[str, Identifier] = field(default_factory=dict)
    indexes: dict[str, int] = field(
        default_factory=lambda: {"static": 0, "field": 0, "arg": 0, "var": 0}
    )

    def start_subroutine(self) -> None:
        """Clears the subroutine symbol table and resets indexes"""

        self.subroutine_table.clear()
        self.indexes["arg"] = 0
        self.indexes["var"] = 0

    def start_class(self) -> None:
        """Clears the symbol table and resets indexes"""

        self.class_table.clear()
        self.indexes["static"] = 0
        self.indexes["field"] = 0
        self.start_subroutine()

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
                print(exist_id)
                raise ValueError(
                    f"{name} already exists in the subroutine table. {exist_id}"
                )

            self.subroutine_table[name] = new_id

    def get(
        self, item: str, default: Optional[Identifier] = None
    ) -> Optional[Identifier]:
        """Get an item from either the class or subroutine table

        Args:
            `item` (str): The item to retrieve
            `default` (str | None): What to return if the item doesn't exist in
                either table

        Returns:
            `item` if in one of the tables, otherwise `default`
        """

        if identifier := self.class_table.get(item):
            return identifier

        if identifier := self.subroutine_table.get(item):
            return identifier

        return default


@dataclass
class Identifier:
    """Dataclass representing a specific row of the `SymbolTable`

    Attributes:
        `name` (str): The name of the identifier
        `data_type` (str): One of 'int', 'bool', 'char', `String`, `Array`, or
            some className defined in the current .jack files
        `category` (str): One of 'var','arg','static','field','class','subroutine'
        `index` (int): The current index based on which symbol table and category
    """

    name: str
    data_type: str
    category: str
    index: int
