"""
Module for accepting user input, parsing arguments, etc.
"""
from __future__ import annotations

from argparse import ArgumentParser, Namespace
from glob import glob
import os
import sys

from exceptions import InvalidOperationException


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


def list_files(directory: str) -> list[str]:
    """Return a list of files that will be analyzed

    Returns:
        `list[str]`: All .jack files in the directory
    """

    return glob(f"{directory}/*.jack")


def start_cli() -> list[str]:
    """Retrieve input from user and return all files to be processed

    Returns:
        `list[str]`: All .jack files to be processed by the analyzer
    """
    args = initialize_argparser()
    file_or_dir = initialize_arguments(args).file_or_dir

    if os.path.isdir(file_or_dir):
        return list_files(file_or_dir)
    return [file_or_dir]


if __name__ == "__main__":
    raise InvalidOperationException("Not intended to be run standalone")
