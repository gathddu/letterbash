from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path

from letterbash.selection import choose_film
from letterbash.watchlist import parse_watchlist


def main(argv: Sequence[str] | None = None) -> int:

    arguments = list(sys.argv[1:] if argv is None else argv)

    if len(arguments) == 2 and arguments[0] in {"import", "pick"}:
        command, raw_watchlist_path = arguments
        watchlist_path = Path(raw_watchlist_path)

        try:
            with watchlist_path.open(encoding="utf-8", newline="") as source:
                entries = parse_watchlist(source)
        except FileNotFoundError:
            print(
                f"letterbash: watchlist not found: {watchlist_path}",
                file=sys.stderr,
            )
            return 1

        if command == "import":
            print(f"watchlist has {len(entries)} films")
            return 0

        try:
            selected = choose_film(entries)
        except ValueError as error:
            print(f"letterbash: {error}", file=sys.stderr)
            return 1

        print(f"{selected.name} ({selected.year})")
        return 0

    print("letterbash: find the film that fits")
    return 0
