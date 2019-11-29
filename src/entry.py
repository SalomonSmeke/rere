"""rere is a regex storage and retrieval tool.

rere can save regex patterns you use frequently and retrieve them later on. rere can also fallback
to an online source for patterns you have not found."""
from io import StringIO
from pathlib import Path
from sys import stderr

from .cli import make_arg_parser, user_bool
from .constants import NAME_MULTIPLEXOR, PATTERN_FILENAME, RC_FILENAME, RERE_HOME
from .easter import gimme_dj
from .filehandling import DataFilesHandler
from .util import delete_file


def main() -> None:
    """Entry, should eventually support non-cli usage."""
    parser = make_arg_parser()
    args = parser.parse_args()
    homepath = Path(RERE_HOME)

    if not homepath.exists():
        print(f"Homepath {homepath} does not exist.", stderr)
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

    elif args.ls:
        print(file_handler.patterns_to_string().strip())

    elif args.jinkies or args.zoinks:
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

    elif args.b:
        print(gimme_dj(args.b[0], args.b[1]))

    elif args.REGULAR_EXPRESSION_NAME:
        pattern = None  # Retrieve step

        if pattern is None:
            exit(1)
        else:
            print(pattern)
    else:
        parser.print_help(stderr)
        exit(1)

    exit(0)
