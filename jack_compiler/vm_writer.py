"""
Module with VMWriter class to hold VM writing state as well as methods
for writing VM language output to file during compilation
"""

from __future__ import annotations

# This is to work through issues when the class grader uses older python
# Like 3.8 which does not have StrEnum
try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        def __str__(self) -> str:
            return self.value


class Segment(StrEnum):
    """
    Represents the 8 memory segments in the VM
    """

    CONST = "constant"
    ARG = "argument"
    LOCAL = "local"
    STATIC = "static"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"


class Arithmetic(StrEnum):
    """
    Represents the 9 arithmetic operations in the VM
    """

    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"


class VMWriter:
    """VMWriter class. Contains methods for writing VM code output to .vm files

    Attributes:

        `_file` (str): .vm file currently being written
        `_if_num` (int): Current number of `if` to write.  For labeling jumps
            in `if-goto` logic
        `_while_num` (int): Current number of `while` to write.  For labeling jumps
            in `while` logic
    """

    def __init__(self, file: str) -> None:
        self._file = file
        # TODO: Might move these to the compiler, as this may be a bad place to keep track of
        # the label counts without broader understanding of the tokens and state
        self._if_num = 0
        self._while_num = 0

    def write_push(self, segment: Segment, index: int) -> str:
        """Writes a VM push command

        Args:
            `segment` (Segment): One of the memory segments:
                - "constant"
                - "argument"
                - "local"
                - "static"
                - "this"
                - "that"
                - "pointer"
                - "temp"
            `index` (int): Index to be pushed
        """

        # Decision: We return a string a to the caller (compilation_engine)
        # which will then write to a deque and then call f.writelines()
        return f"push {segment} {index}\n"

    def write_pop(self, segment: Segment, index: int) -> str:
        """Writes a VM pop command

        Args:
            `segment` (Segment): One of the memory segments:
                - "constant"
                - "argument"
                - "local"
                - "static"
                - "this"
                - "that"
                - "pointer"
                - "temp"
            `index` (int): Index to be popped
        """

        return f"push {segment} {index}\n"

    def write_arithmetic(self, command: Arithmetic) -> None:
        # TODO: Implement math logic
        pass

    def write_label(self, label: str) -> str:
        """Writes a VM label
        e.g.: `label LABEL`

        Args:
            `label` (str): The label name
        """

        return f"label {label}\n"

    def write_goto(self, label: str) -> str:
        """Writes a VM goto
        e.g.: `goto LABEL`

        Args:
            `label` (str): The label name to `goto`
        """

        return f"goto {label}\n"

    def write_if(self, label: str) -> str:
        """Writes a VM if-goto
        e.g.: `if-goto LABEL`

        Args:
            `label` (str): The label name to `goto` on the if condition
        """

        return f"if-goto {label}\n"

    def write_call(self, name: str, n_args: int) -> str:
        """Writes a VM function call
        e.g.: `call functionName nArgs`

        Args:
            `name` (str): The function to be called
                (will only be `className.functionName`, either a method or function depending on the implicit this argument)
            `n_args` (int): The number of arguments being passed to the function
                call
        """

        return f"call {name} {n_args}\n"

    def write_function(self, name: str, n_locals: int) -> str:
        """Writes a VM function definition
        e.g.: `function functionName nLocals`

        Args:
            `name` (str): The function to be declared
                (will only be `className.functionName`, either a method or function depending on the implicit this argument)
            `n_locals` (int): The number of arguments being passed to the function
                definition
        """

        return f"call {name} {n_locals}\n"

    def write_return(self) -> str:
        """Writes vm return"""
        return "return\n"

    # IF STATEMENT:
    # if (~(next = null))
    # {
    #     do data.dispose();
    #     let data = next.getData();
    #     let previous = next;
    #     let next = next.getNext();
    #
    #     // Prevent a memory leak by disposing of the node that's moved up
    #     do previous.setNext(null);
    #     do previous.dispose();
    # }
    # else
    # {
    #     do data.dispose();
    #     let data = null;
    # }

    # push this 1
    # push constant 0
    # eq
    # not
    # if-goto IF_TRUE1
    # goto IF_FALSE1
    # label IF_TRUE1
    # push this 0
    # call Invader.dispose 1
    # pop temp 0
    # push this 1
    # call InvaderList.getData 1
    # pop this 0
    # push this 1
    # pop local 0
    # push this 1
    # call InvaderList.getNext 1
    # pop this 1
    # push local 0
    # push constant 0
    # call InvaderList.setNext 2
    # pop temp 0
    # push local 0
    # call InvaderList.dispose 1
    # pop temp 0
    # goto IF_END1
    # label IF_FALSE1
    # push this 0
    # call Invader.dispose 1
    # pop temp 0
    # push constant 0
    # pop this 0
    # label IF_END1
