"""Useful constants for rere."""
from os import getenv
from pathlib import Path
from typing import Dict, Union

# rere config constants
DEFAULT_LOOKUP_LOCATION = (
    "https://raw.githubusercontent.com/SalomonSmeke/rere/dev/assets/basic.rere"
)
VALUES_SEPARATOR = ":"
NAME_MULTIPLEXOR = "|"
CONFIG_NAMES_AND_DEFAULTS: Dict[str, Union[bool, str]] = {
    "should_lookup": True,
    "should_save": True,
    "lookup_location": DEFAULT_LOOKUP_LOCATION,
}
RC_FILENAME = getenv("RERERC_NAME", ".rererc")
PATTERN_FILENAME = getenv("RERE_PATTERNFILE_NAME", ".rerepatterns")
RERE_HOME = getenv("RERE_HOME", str(Path.home()))

# argparse constants
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

# secrets
# pylint: disable=C0301
B = b"ICAgIF9fXwogLCB8IGwgfCAKKCggfCBsIHwgKSkKICAgfCBsIHwgJwogICAgXF8vCiAgIC8uLi5c\nLS0uICAgXyAgCiAgID09PT09ICBgLS0oXz0=\n"
