"""Utilities related to the rererc config file"""
from typing import NamedTuple, Union, List, Dict, Tuple, DefaultDict
from typing import TextIO
from collections import defaultdict
from prompt import user_bool, user_string
from constants import (
    DEFAULT_LOOKUP_LOCATION,
    PATTERN_INDICATOR,
    CONFIG_VALUES_INDICATOR,
    CONFIG_NAMES_AND_DEFAULTS,
    VALUES_SEPARATOR,
    NAME_MULTIPLEXOR,
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
        else user_string(
            f"Where would you like to look for regex patterns?"
        )
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


def _parse_config_and_patterns(raw: TextIO) -> Tuple[Config, Dict[str, str]]:
    """Get Config and pattern dict from a rererc file."""
    patterns = {}
    config_found = False
    config = {k: v for k, v in CONFIG_NAMES_AND_DEFAULTS.items()}

    for line in raw:
        if line[0] == CONFIG_VALUES_INDICATOR:
            ckey = line[1:].split(VALUES_SEPARATOR)[0]
            cval: Union[str, bool] = VALUES_SEPARATOR.join(line.split(VALUES_SEPARATOR)[1:]).strip()

            if ckey.startswith("should"):
                cval = cval == "true"

            config_found = True
            config[ckey] = cval
        elif line[0] == PATTERN_INDICATOR:
            value = VALUES_SEPARATOR.join(line[1:].split(VALUES_SEPARATOR)[1:]).rstrip()
            for name in line[1:].split(VALUES_SEPARATOR)[0].split(NAME_MULTIPLEXOR):
                patterns[name.strip()] = value

    return (
        Config(
            config["should_lookup"],  # type: ignore
            config["should_save"],  # type: ignore
            config["lookup_location"],  # type: ignore
            config_found,
        ),
        patterns,
    )


class RereRC:
    def __init__(self, file: TextIO, path: str) -> None:
        self.config, self.patterns = _parse_config_and_patterns(file)

    def __contains__(self, name: Union[str, List[str]]) -> bool:
        search = [name] if isinstance(name, str) else [p for p in name]
        return next((True for name in search if name.strip() in self.patterns), False)

    def configure(self) -> None:
        self.config = _make_user_config()

    def get_pattern(self, name: Union[str, List[str]]) -> str:
        search = [name] if isinstance(name, str) else [p for p in name]

        try:
            found = next(name.strip() for name in search if name.strip() in self.patterns)
        except StopIteration:
            raise KeyError(name)

        return self.patterns[found]

    def set_pattern(self, name: Union[str, List[str]], pattern: str) -> None:
        pattern = pattern.strip().replace("\n", "\\n")

        for fragment in [name] if isinstance(name, str) else [p for p in name]:
            self.patterns[fragment.strip()] = pattern

    def remove_pattern(self, name: Union[str, List[str]]) -> None:
        for fragment in [name] if isinstance(name, str) else [p for p in name]:
            self.patterns.pop(fragment.strip(), None)

    def should_save_config(self) -> bool:
        return self.config.user_generated

    def export_config(self) -> str:
        return (
            f"^should_lookup{VALUES_SEPARATOR}{self.config.should_lookup}\n"
            f"^should_save{VALUES_SEPARATOR}{self.config.should_save}\n"
            f"^lookup_location{VALUES_SEPARATOR}{self.config.lookup_location}"
        )

    def export_patterns(self) -> str:
        patterns = self.patterns
        inverse_pattern_table: DefaultDict[str, List[str]] = defaultdict(list)

        for name, pattern in patterns.items():
            inverse_pattern_table[pattern].append(name)

        return "\n".join(
            [
                f"!{NAME_MULTIPLEXOR.join(names)}{VALUES_SEPARATOR}{pattern}"
                for pattern, names in inverse_pattern_table.items()
            ]
        )
