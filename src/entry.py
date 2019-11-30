"""rere is a regex storage and retrieval tool.

rere can save regex patterns you use frequently and retrieve them later on. rere can also fallback
to an online source for patterns you have not found."""
import argparse
from io import StringIO
from pathlib import Path
from sys import stderr

from urllib3 import PoolManager

from .cli import make_arg_parser, user_bool
from .constants import NAME_MULTIPLEXOR, PATTERN_FILENAME, RC_FILENAME, RERE_HOME
from .easter import gimme_dj
from .filehandling import DataFilesHandler
from .util import delete_file


def add(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
    file_handler: DataFilesHandler,
    homepath: Path
) -> None:
    """Broken-out logic path for adding a new pattern"""
    name = NAME_MULTIPLEXOR.join(args.REGULAR_EXPRESSION_NAME)

    if not name:
        parser.print_help(stderr)
        exit(1)

    if file_handler.has_pattern(name) and not args.force:
        if not user_bool(
            (
                f"{name} already exists as {file_handler.get_pattern(name)} do you want to "
                f"override it? "
            )
        ):
            exit(1)

    file_handler.set_pattern(name, args.add)
    file_handler.flush(str(homepath), patterns=True)
    print(args.add)


def delete_files(
    args: argparse.Namespace,
    file_handler: DataFilesHandler,
    pattern_filepath: Path,
    config_filepath: Path
) -> None:
    """Broken out logic for deleting rere files"""
    if pattern_filepath.exists():
        if not args.force and not user_bool(
            "Are you sure you want to delete your patternfile? "
        ):
            exit(1)

        delete_file(pattern_filepath)

    if args.jinkies:
        print(file_handler.patterns_to_string())

    if args.zoinks and config_filepath.exists():
        if not args.force and not user_bool("Are you sure you want to delete your rererc? "):
            exit(1)

        delete_file(config_filepath)


def retrieve(
    args: argparse.Namespace,
    file_handler: DataFilesHandler,
    homepath: Path
) -> str:
    """Find an expression by name."""
    name = NAME_MULTIPLEXOR.join(args.REGULAR_EXPRESSION_NAME)

    try:
        return file_handler.get_pattern(name)
    except KeyError:
        pass

    if args.local or (not file_handler.config.should_lookup and not args.online):
        print(f"{name} not found locally, lookups disabled.", file=stderr)
        exit(1)

    external_patterns = PoolManager().request(
        "GET",
        file_handler.config.lookup_location
    ).data.decode('utf-8')

    try:
        pattern = DataFilesHandler(StringIO(), StringIO(external_patterns)).get_pattern(name)
    except KeyError:
        print(f"{name} not found at {file_handler.config.lookup_location} or locally.", file=stderr)
        exit(1)

    if args.save or (file_handler.config.should_save and not args.no_save):
        file_handler.set_pattern(name, pattern)
        file_handler.flush(str(homepath), patterns=True)

    return pattern


def main() -> None:
    """Entry, should eventually support non-cli usage."""
    parser = make_arg_parser()
    args = parser.parse_args()
    homepath = Path(RERE_HOME)

    if not homepath.exists():
        print(f"Homepath {homepath} does not exist.", file=stderr)
        exit(1)

    config_filepath = homepath.joinpath(RC_FILENAME)
    pattern_filepath = homepath.joinpath(PATTERN_FILENAME)
    config_stream = open(str(config_filepath), "r") if config_filepath.exists() else StringIO()
    pattern_stream = open(str(pattern_filepath), "r") if pattern_filepath.exists() else StringIO()
    file_handler = DataFilesHandler(config_stream, pattern_stream)

    config_stream.close()
    pattern_stream.close()

    if args.init:
        file_handler.configure(str(homepath))

    elif args.add:
        add(parser, args, file_handler, homepath)

    elif args.ls:
        print(file_handler.patterns_to_string().strip())

    elif args.jinkies or args.zoinks:
        delete_files(args, file_handler, pattern_filepath, config_filepath)

    elif args.b:
        print(gimme_dj(args.b[0], args.b[1]))

    elif args.REGULAR_EXPRESSION_NAME:
        print(retrieve(args, file_handler, homepath))

    else:
        parser.print_help(stderr)
        exit(1)

    exit(0)
