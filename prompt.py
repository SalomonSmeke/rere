"""Utilities for chatting with you."""
from typing import Optional, Set


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
