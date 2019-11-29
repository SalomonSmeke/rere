"""Handy functions"""
from os import remove
from pathlib import Path


def delete_file(path: Path) -> None:
    """Delete a file if it exists"""
    try:
        if path.exists:
            remove(str(path))
    except OSError:
        pass
