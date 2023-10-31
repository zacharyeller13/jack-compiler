"""
Module for accepting user input, parsing arguments, etc.
"""

from argparse import ArgumentParser, Namespace
import os
import sys


class InvalidOperationException(Exception):
    """Operation is invalid
    """


def initialize_argparser() -> ArgumentParser:
    """Initialize ArgumentParser for command-line arguments

    Returns:
        `ArgumentParser`
    """

    arg_parser = ArgumentParser(
        prog="JackAnalzyer",
        description="Analyze .jack file(s) and output as\
            .xml file(s) to be used in a larger Jack Compiler",
    )
    arg_parser.add_argument(
        "file_or_dir",
        metavar="file.jack or /dirname/",
        type=str,
        help="absolute filepath of the .vm file or directory to be analyzed",
    )

    return arg_parser


def initialize_arguments(arg_parser: ArgumentParser) -> Namespace:
    """Parse command-line arguments

    Args:
        `arg_parser` (ArgumentParser): An arg parsing object

    Returns:
        `Namespace`: Store of command line arguments/attributes
    """

    arg_namespace = arg_parser.parse_args()

    if arg_namespace.file_or_dir[-4:] != ".jack" and not os.path.isdir(
        arg_namespace.file_or_dir
    ):
        arg_parser.print_usage()
        sys.exit()

    return arg_namespace


def read_files() -> list[str]:
    raise NotImplementedError


if __name__ == "__main__":
    raise InvalidOperationException("Not intended to be run standalone")
