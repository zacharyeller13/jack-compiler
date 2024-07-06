"""
Module with VMWriter class to hold VM writing state as well as methods
for writing VM language output to file during compilation
"""


class VMWriter:
    """VMWriter class. Contains methods for writing VM code output to .vm files

    Attributes:

        `_file` (str): .vm file currently being written
        `_if_num` (int): Current number of `if` to write.  For labeling jumps
            in `if-goto` logic
        `_while_num` (int): Current number of `while` to write.  For labeling jumps
            in `while` logic
    """

    def __init__(self):
        pass

    # WHILE STATEMENT:
    # label WHILE_EXP0
    # push local 0
    # push constant 0
    # eq
    # not
    # not
    # if-goto WHILE_END0
    # push local 0
    # call InvaderList.getData 1
    # pop local 1
    # push local 1
    # push constant 0
    # eq
    # not
    # if-goto IF_TRUE0
    # goto IF_FALSE0
    # label IF_TRUE0
    # push local 1
    # call Invader.move 1
    # pop temp 0
    # label IF_FALSE0
    # push local 0
    # call InvaderList.getNext 1
    # pop local 0
    # goto WHILE_EXP0
    # label WHILE_END0

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
