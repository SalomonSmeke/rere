"""Utilities for user interaction"""
from argparse import ArgumentParser
from typing import Optional, Set

from .constants import ARGPARSE_DESCRIPTION, ARGPARSE_EPILOG


def make_arg_parser() -> ArgumentParser:
    """Set up CLI args and options."""
    parser = ArgumentParser(description=ARGPARSE_DESCRIPTION, epilog=ARGPARSE_EPILOG)

    parser.add_argument(
        "--init", "-i", help="Run first-time setup/config wizard.", action="store_true"
    )
    parser.add_argument(
        "--add",
        "-a",
        metavar="REGEX PATTERN",
        help="Adds the pattern to your stored patterns.",
        type=str,
    )
    parser.add_argument(
        "--remove", "-r", help="Remove the pattern from your stored patterns.", action="store_true"
    )
    parser.add_argument(
        "--force", "-f", help="Skip confirmation for -a, -j and -z.", action="store_true"
    )
    parser.add_argument(
        "--local",
        "-l",
        help="Do not perform an external search if the pattern is not found locally.",
        action="store_true",
    )
    parser.add_argument(
        "--online",
        "-o",
        help="Perform an external search if the pattern is not found locally.",
        action="store_true",
    )
    parser.add_argument(
        "--no-save",
        "-n",
        help="Prevent the pattern from saving, if it is looked up externally.",
        action="store_true",
    )
    parser.add_argument(
        "--save", "-s", help="Save the pattern if it is looked up externally.", action="store_true"
    )
    parser.add_argument(
        "--ls",
        "--list",
        help="Print your saved patterns in patternfile format.",
        action="store_true",
    )
    parser.add_argument(
        "--jinkies",
        "-j",
        help="Delete the rere patterns, output the file to stdout.",
        action="store_true",
    )
    parser.add_argument(
        "--zoinks", "-z", help="Delete the rererc and patternfile silently.", action="store_true"
    )
    parser.add_argument(
        "REGULAR_EXPRESSION_NAME",
        help="Name or search term for an expression. Multiple allowed.",
        type=str,
        nargs="*",
    )
    parser.add_argument("-b", type=int, metavar="?", nargs="*")

    return parser


def user_bool(prompt: str) -> bool:
    """Get a boolean from the user"""
    lookup = {"y": True, "yes": True, "n": False, "no": False}
    options = "[y/n]: "
    value = input(f"{prompt} {options}    ").lower().strip()

    while True:
        if value in lookup:
            return lookup[value]

        print(f"Please enter {options}")
        value = input(f"{prompt}:    ").lower().strip()


def user_string(
    prompt: str, allow_empty: bool = False, disallowed_values: Optional[Set[str]] = None
) -> str:
    """Get a string from the user"""
    value = input(f"{prompt}    ").strip()

    while True:
        if disallowed_values is not None and next(
            (True for c in value if c in disallowed_values), False
        ):
            print(f"Invalid input, must not contain: {repr(list(disallowed_values))}.")
        elif not value and not allow_empty:
            print(f"Input must not be empty.")
        else:
            return value

        value = input(f"{prompt}    ").strip()
