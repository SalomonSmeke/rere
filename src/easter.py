"""Nothing nefarious or useful"""
from .constants import B


def gimme_dj(mystery_val: int, secret_val: int) -> str:
    """Play that funky music."""
    # If youre worried about what this is doing, and NEED TO KNOW. Check this gist:
    # https://gist.github.com/SalomonSmeke/2dfef1f714851ae8c6933c71dad701ba
    # its nothing evil. just an inside joke for my good buddy Brian.
    from importlib import import_module

    hey: str = getattr(
        import_module("".join(chr(c + secret_val) for c in [29, 28, 46, 32, -15, -17])),
        "".join(
            chr(c - (mystery_val % secret_val))
            for c in [106, 107, 105, 117, 106, 107, 104, 127, 122, 107, 121]
        ),
    )(B)
    brian: str = getattr(
        hey, "".join(chr(c - (503 - mystery_val)) for c in [183, 184, 182, 194, 183, 184])
    )("".join(chr(c) for c in [117, 116, 102, 45, 56]))
    return brian
