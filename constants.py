"""Useful constants for rere."""
from os import getenv
from pathlib import Path

DEFAULT_LOOKUP_LOCATION = (
    "https://raw.githubusercontent.com/SalomonSmeke/rere/dev/patternfiles/basic.rere"
)

VALUES_SEPARATOR = ":"
NAME_MULTIPLEXOR = "|"
PATTERN_INDICATOR = "!"
CONFIG_VALUES_INDICATOR = "^"
CONFIG_NAMES_AND_DEFAULTS = {
    "should_lookup": True,
    "should_save": True,
    "lookup_location": DEFAULT_LOOKUP_LOCATION,
}
RERE_HOME: str = getenv("RERE_HOME", str(Path.home()))

ARGPARSE_DESCRIPTION = (
    f"rere is a regex storage and retrieval tool. rere can save regex patterns you use frequently "
    f"and retrieve them later on. rere can also fallback to an online source for patterns you have "
    f"not stored."
)

ARGPARSE_EPILOG = (
    f"The .rererc file is created in your ${{RERE_HOME:-$HOME}} directory if it does not exist the "
    f"first time an entry is inserted. This may happen from an --add call or an external lookup "
    f"at which point you will be prompted for its initial values. You can change these anytime by "
    f"editing the file directly, or running the config wizard."
    f"NOTE: certain special characters are not allowed in pattern names ['{VALUES_SEPARATOR}', "
    f"'{NAME_MULTIPLEXOR}', '*']."
)
