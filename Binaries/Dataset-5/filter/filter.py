#!/usr/bin/env python
#
# Setup:
#    apt install cpp
#    pip install pycparser

from argparse import ArgumentParser
import glob
import logging
import os
import pycparser
import sys

log = logging.getLogger()


def find_nodes_by_type(node, filter_type):
    """Generator that returns all nodes of the specified type (recursive)."""
    if isinstance(node, filter_type):
        hits = [node]
    else:
        hits = []

    for c in node:
        hits += find_nodes_by_type(c, filter_type)

    return hits


def parse_c_file(fp):
    """Parses a C file and returns an AST."""
    cpp_args = list()

    # add fake headers to includes
    fake_includes_fp = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fake_libc_include"
    )
    cpp_args.append("-I%s" % fake_includes_fp)

    # we nullify compiler extensions like __attribute__ because pycparser cannot handle them and
    # we don't need them since we aren't compiling to machine code
    cpp_args += [
        "-D",
        "__attribute__(x)=",
        "-D",
        "__extension__=",
        "-D",
        "__restrict=",
    ]

    log.debug("cpp arguments: %s" % str(cpp_args))

    return pycparser.parse_file(fp, use_cpp=True, cpp_args=cpp_args)


def init_logging(options):
    log.setLevel(options.logging)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(levelname)7s | %(asctime)15s " "| %(message)s")
    )
    log.addHandler(handler)


def parse_arguments():
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "-l",
        "--logging",
        action="store",
        type=int,
        default=20,
        help="Log level [10-50] (default: 20 - Info)",
    )
    arg_parser.add_argument(
        "target_directory",
        action="store",
        type=str,
        help="Directory used as output for atcoder.py",
    )

    return arg_parser.parse_args()


def main():
    options = parse_arguments()
    init_logging(options)

    if not os.path.isdir(os.path.realpath(options.target_directory)):
        log.error(
            "Target directory does not exist or is not a directory: %s"
            % options.target_directory
        )
        sys.exit(1)

    for fp in glob.iglob(options.target_directory + "/**/*.c", recursive=True):
        log.debug("Parsing: %s" % fp)

        try:
            ast = parse_c_file(fp)
        except pycparser.plyparser.ParseError as ex:
            log.error("Failed to parse: %s" % fp)
            log.error("Exception: %s" % str(ex))

        func_defs = find_nodes_by_type(ast, pycparser.c_ast.FuncDef)

        helper_funcs = False
        for func in func_defs:
            if func.decl.name != "main":
                helper_funcs = True
                break

        if helper_funcs:
            log.info("Deleting: %s" % fp)
            os.remove(fp)


if __name__ == "__main__":
    main()
