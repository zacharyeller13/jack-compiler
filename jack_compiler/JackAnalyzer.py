# pylint: disable=invalid-name
"""
JackAnalyzer program.  Does not conform to snake case naming convention
in order to comply with submission rules of the Nand2Tetris course.
"""

from __future__ import annotations
from jack_compiler.cli import start_cli
from jack_compiler.compilation_engine_xml import CompilationEngineXml


def main() -> None:
    files_to_tokenize = start_cli()

    # for file in files_to_tokenize:
    #     filename = file[:-5]
    #     tokens = parse_file(file)
    #     print(tokens)
    #     write_tokens_file(filename + "T", tokens)

    engine = CompilationEngineXml(files_to_tokenize)
    engine.compile_all()


if __name__ == "__main__":
    main()
