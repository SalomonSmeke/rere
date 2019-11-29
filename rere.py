"""rere is a regex storage and retrieval tool.

rere can save regex patterns you use frequently and retrieve them later on. rere can also fallback
to an online source for patterns you have not found."""
import argparse
from sys import stderr
from pathlib import Path
from io import StringIO
from constants import ARGPARSE_DESCRIPTION, ARGPARSE_EPILOG, RERE_HOME
from rc import RereRC


def setup_argparse() -> argparse.ArgumentParser:
    """Set up CLI args and options."""
    parser = argparse.ArgumentParser(description=ARGPARSE_DESCRIPTION, epilog=ARGPARSE_EPILOG)

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
        "--force",
        "-f",
        help="If the pattern you are trying to add already exists, overwrite it.",
        action="store_true",
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
        "--export",
        "-e",
        help="Export your saved patterns from .rererc to ./export.txt.",
        action="store_true",
    )
    parser.add_argument(
        "--jinkies",
        "-j",
        help="Delete the rere config, output the file to stdout.",
        action="store_true",
    )
    parser.add_argument(
        "--zoinks", "-z", help="Delete the rere config silently.", action="store_true"
    )
    parser.add_argument(
        "REGULAR_EXPRESSION_NAME",
        help="Name or search term for an expression. Multiple allowed.",
        type=str,
        nargs="*",
    )
    parser.add_argument("-b", help="it must do something", action="store_true")

    return parser


def entry() -> None:
    """Pick-a-pipe."""
    parser = setup_argparse()
    args = parser.parse_args()

    rc_path = Path(RERE_HOME).joinpath(".rererc")
    rererc = None
    if rc_path.exists():
        with open(str(rc_path), "r") as file:
            rererc = RereRC(file, str(rc_path))
    else:
        rererc = RereRC(StringIO(), str(rc_path))

    if args.init:
        rererc.configure()
    elif args.add:
        add_pattern(
            args.add,
            args.force,
            local=args.local,
            online=args.online,
            no_save=getattr(args, "no-save"),
            save=args.save,
        )
    elif args.export:
        pass
    elif args.jinkies:
        pass
    elif args.zoinks:
        pass
    elif args.b:
        pass
    else:
        parser.print_help(stderr)
        exit(1)

    exit(0)
