"""
Module with VMWriter class to hold VM writing state as well as methods
for writing VM language output to file during compilation
"""

from enum import Enum


class VMWriter:
    """VMWriter class. Contains methods for writing VM code output to .vm files

    Attributes:

        `_file` (str): .vm file currently being written
        `_if_num` (int): Current number of `if` to write.  For labeling jumps
            in `if-goto` logic
        `_while_num` (int): Current number of `while` to write.  For labeling jumps
            in `while` logic
    """

    def __init__(self) -> None:
        # TODO: Define constructor
        pass

    def write_push(self) -> None:
        # TODO: Implement push logic
        pass

    def write_pop(self) -> None:
        # TODO: Implement pop logic
        pass

    def write_arithmetic(self) -> None:
        # TODO: Implement math logic
        pass

    def write_label(self) -> None:
        # TODO: Implement label logic
        pass

    def write_goto(self) -> None:
        # TODO: Implement goto logic
        pass

    def write_if(self) -> None:
        # TODO: Implement if logic
        pass

    def write_call(self) -> None:
        # TODO: Implement call logic
        pass

    def write_function(self) -> None:
        # TODO: Implement function logic
        pass

    def write_return(self) -> None:
        # TODO: Implement return logic
        pass

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


class Segment(str, Enum):
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


class Arithmetic(str, Enum):
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
