# pylint: disable=invalid-name
"""
JackAnalyzer program.  Does not conform to snake case naming convention
in order to comply with submission rules of the Nand2Tetris course.
"""
from __future__ import annotations
from cli import start_cli
from tokenizer import parse_file
from token_writer import write_tokens_file


def main() -> None:
    files_to_tokenize = start_cli()

    for file in files_to_tokenize:
        filename = file[:-5]
        tokens = parse_file(file)
        print(tokens)
        write_tokens_file(filename+'T', tokens)


if __name__ == "__main__":
    main()
