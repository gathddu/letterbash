from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path

from letterbash.selection import choose_film
from letterbash.watchlist import parse_watchlist


def main(argv: Sequence[str] | None = None) -> int:

    arguments = list(sys.argv[1:] if argv is None else argv)

    if len(arguments) == 2 and arguments[0] == "import":
        watchlist_path = Path(arguments[1])
        with watchlist_path.open(encoding="utf-8", newline="") as source:
            entries = parse_watchlist(source)

        print(f"watchlist has {len(entries)} films")
        return 0

    if len(arguments) == 2 and arguments[0] == "pick":
        watchlist_path = Path(arguments[1])
        with watchlist_path.open(encoding="utf-8", newline="") as source:
            entries = parse_watchlist(source)

        selected = choose_film(entries)
        print(f"{selected.name} ({selected.year})")
        return 0

    print("letterbash: find the film that fits")
    return 0
