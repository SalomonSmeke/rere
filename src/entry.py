"""rere is a regex storage and retrieval tool.

rere can save regex patterns you use frequently and retrieve them later on. rere can also fallback
to an online source for patterns you have not found."""
import argparse
from sys import stderr
from os import remove
from pathlib import Path
from io import StringIO
from .constants import ARGPARSE_DESCRIPTION, ARGPARSE_EPILOG, RERE_HOME, B
from .rc import RereRC
from .prompt import user_bool


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
    parser.add_argument(
        "-b",
        type=int,
        metavar="?",
    )

    return parser

def add_pattern(name: str, pattern: str, force: bool, rererc: RereRC) -> bool:
    if name in rererc and not force:
        if not user_bool(
            f"{name} already exists as {rererc.get_pattern(name)} do you want to override it? "
        ):
            return False

    rererc.set_pattern(name, pattern)
    return True

def export(rererc: RereRC) -> None:
    print(rererc.export_patterns())

def print_rererc(rererc: RereRC) -> None:
    print(rererc.export_config())
    print(rererc.export_patterns())

def delete_file(path: Path) -> None:
    try:
        if path.exists:
            remove(str(path))
    except OSError:
        pass

def gimme_dj(mystery_val: int) -> None:
    """Play that funky music."""
    # If youre worried about what this is doing, and NEED TO KNOW. Check this gist:
    # https://gist.github.com/SalomonSmeke/2dfef1f714851ae8c6933c71dad701ba
    # its nothing evil. just an inside joke for my good buddy Brian.
    from importlib import import_module
    hey: str = getattr(
        import_module("".join(chr(c) for c in [98, 97, 115, 101, 54, 52])),
        "".join(chr(c) for c in [100, 101, 99, 111, 100, 101, 98, 121, 116, 101, 115]),
    )(B)
    brian: str = getattr(
        hey, "".join(chr(c - (503 - mystery_val)) for c in [183, 184, 182, 194, 183, 184])
    )("".join(chr(c) for c in [117, 116, 102, 45, 56]))
    print(brian)

def main() -> None:
    parser = setup_argparse()
    args = parser.parse_args()

    rc_path = Path(RERE_HOME).joinpath(".rererc")
    rererc = None
    if rc_path.exists():
        with open(str(rc_path), "r") as file:
            rererc = RereRC(file, str(rc_path))
    else:
        rererc = RereRC(StringIO(), str(rc_path))

    if args.init: # type: ignore
        rererc.configure()
    elif args.add: # type: ignore
        if not args.REGULAR_EXPRESSION_NAME: # type: ignore
            parser.print_help(stderr)
            exit(1)

        add_pattern(args.REGULAR_EXPRESSION_NAME, args.add, args.force, rererc) # type: ignore
    elif args.export: # type: ignore
        export(rererc)
    elif args.jinkies: # type: ignore
        if rc_path.exists():
            print_rererc(rererc)

        delete_file(rc_path)
    elif args.zoinks: # type: ignore
        delete_file(rc_path)
    elif args.b: # type: ignore
        gimme_dj(args.b)
    elif args.REGULAR_EXPRESSION_NAME: # type: ignore
        pass
    else:
        parser.print_help(stderr)
        exit(1)

    exit(0)
