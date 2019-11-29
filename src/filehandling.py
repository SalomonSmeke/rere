"""Utilities related to the rererc files"""
from collections import OrderedDict
from pathlib import Path
from typing import List  # pylint: disable=unused-import
from typing import NamedTuple, TextIO

from .cli import user_bool, user_string
from .constants import (
    CONFIG_NAMES_AND_DEFAULTS,
    DEFAULT_LOOKUP_LOCATION,
    NAME_MULTIPLEXOR,
    PATTERN_FILENAME,
    RC_FILENAME,
    VALUES_SEPARATOR,
)


class Config(NamedTuple):
    """A rererc config, and wether it is user-generated or defaulted."""

    should_lookup: bool
    should_save: bool
    lookup_location: str
    user_generated: bool


def _make_user_config() -> Config:
    """Set-up rere with user preferences."""
    should_lookup = user_bool(
        (
            f"Should rere lookup patterns that you do not have locally? (you can specify the lookup"
            f" source later)"
        )
    )
    should_save = (
        False
        if not should_lookup
        else user_bool(
            f"Should patterns that you do not have locally that are looked-up get saved by default?"
        )
    )
    custom_location = (
        False
        if not should_lookup
        else user_bool(
            (
                f"The default lookup location for non-local patterns is: {DEFAULT_LOOKUP_LOCATION}"
                f", would you like to change this?"
            )
        )
    )
    lookup_location = (
        DEFAULT_LOOKUP_LOCATION
        if not custom_location
        else user_string(f"Where would you like to look for regex patterns?")
    )

    print("Thank you! rere is configured. Here is a summary:")
    print(f"\trere will{'' if should_lookup else ' not'} use external lookups.")
    print(f"\trere will{'' if should_save else ' not'} save looked-up patterns.")
    print(
        f"\trere will look for unknown patterns at {lookup_location}."
        if should_lookup
        else "\trere has stored the default lookup_location for --online forced queries."
    )

    return Config(should_lookup, should_save, lookup_location, True)


def _parse_patternfile(raw: TextIO) -> "OrderedDict[str, str]":
    """Take a patternfile and produce a OrderedDict of names to patterns"""
    patterns: "OrderedDict[str, str]" = OrderedDict()

    for line in raw:
        line = line.strip()

        if not line or line[0] == "#":
            continue

        split_line = line.split(VALUES_SEPARATOR)
        pattern = VALUES_SEPARATOR.join(split_line[1:]).rstrip()
        split_names = [name.strip() for name in split_line[0].split(NAME_MULTIPLEXOR)]

        for name in split_names:
            patterns[name] = pattern

    return patterns


def _parse_rererc(raw: TextIO) -> Config:
    """Take a rererc file and produce a Config"""
    config = {
        "should_lookup": CONFIG_NAMES_AND_DEFAULTS["should_lookup"],
        "should_save": CONFIG_NAMES_AND_DEFAULTS["should_save"],
        "lookup_location": CONFIG_NAMES_AND_DEFAULTS["lookup_location"],
        "user_generated": False,
    }

    for line in raw:
        line = line.strip()

        if not line or line[0] == "#" or ":" not in line:
            continue

        split_line = line.split(VALUES_SEPARATOR)

        if split_line[0] in {"should_lookup", "should_save"}:
            config[split_line[0]] = bool(len(split_line[1]))
        elif split_line[0] == "lookup_location":
            config[split_line[0]] = "VALUES_SEPARATOR".join(split_line[1:]).strip()
        else:
            continue

        config["user_generated"] = True

    return Config(
        bool(config["should_lookup"]),
        bool(config["should_save"]),
        str(config["lookup_location"]),
        bool(config["user_generated"]),
    )


class DataFilesHandler:
    """Utility class to manage the rererc and pattern files"""

    def __init__(self, config_file: TextIO, pattern_file: TextIO) -> None:
        self.config: Config = _parse_rererc(config_file)
        self.patterns = _parse_patternfile(pattern_file)

    def flush(self, path_str: str, config: bool = False, patterns: bool = False) -> None:
        """Write changed values to file"""
        path = Path(path_str)
        if config:
            config_content = self.config_to_string()
            config_filepath = str(path.joinpath(RC_FILENAME))
            with open(config_filepath, "w+") as file:
                file.write(f"{config_content}\n")

        if patterns:
            patterns_content = self.patterns_to_string()
            pattern_filepath = str(path.joinpath(PATTERN_FILENAME))
            with open(pattern_filepath, "w+") as file:
                file.write(f"{patterns_content}\n")

    def configure(self, homepath: str) -> None:
        """Run the CLI config wizard, and save the config."""
        self.config = _make_user_config()
        self.flush(homepath, config=True)

    def has_pattern(self, name: str) -> bool:
        """Check if a pattern is registered to a name"""
        search = filter(lambda n: bool(n.strip()), name.split(NAME_MULTIPLEXOR))
        return next((True for n in search if n in self.patterns), False)

    def get_pattern(self, name: str) -> str:
        """Find a pattern by name"""
        search = filter(lambda n: bool(n.strip()), name.split(NAME_MULTIPLEXOR))

        try:
            found = next(name for name in search if name in self.patterns)
        except StopIteration:
            raise KeyError(name)

        return str(self.patterns[found])

    def set_pattern(self, name: str, pattern: str) -> None:
        """Set a pattern by name"""
        pattern = pattern.strip().replace("\n", "\\n")

        for fragment in filter(lambda n: bool(n.strip()), name.split(NAME_MULTIPLEXOR)):
            self.patterns[fragment] = pattern

    def delete_pattern(self, name: str) -> None:
        """Delete a pattern by name"""
        for fragment in filter(lambda n: bool(n.strip()), name.split(NAME_MULTIPLEXOR)):
            self.patterns.pop(fragment, None)

    def config_to_string(self) -> str:
        """Convert the config into a rererc formatted string"""
        return (
            f"should_lookup{VALUES_SEPARATOR}{'1' if self.config.should_lookup else ''}\n"
            f"should_save{VALUES_SEPARATOR}{'1' if self.config.should_save else ''}\n"
            f"lookup_location{VALUES_SEPARATOR}{self.config.lookup_location}"
        )

    def patterns_to_string(self) -> str:
        """Convert the patterns into a patternfile formatted string"""
        patterns = self.patterns
        inverse_pattern_table: "OrderedDict[str, List[str]]" = OrderedDict()

        for name, pattern in patterns.items():
            if pattern not in inverse_pattern_table:
                inverse_pattern_table[pattern] = []

            inverse_pattern_table[pattern].append(name)

        return "\n".join(
            [
                f"{NAME_MULTIPLEXOR.join(names)}{VALUES_SEPARATOR}{pattern}"
                for pattern, names in inverse_pattern_table.items()
            ]
        )
