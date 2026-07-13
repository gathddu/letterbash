"""terminal entry point for letterbash"""

from __future__ import annotations
import sys
from collections.abc import Sequence
from pathlib import Path
from letterbash.watchlist import parse_watchlist


def main(argv: Sequence[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)

    if len(arguments) == 2 and arguments[0] == "import":
        watchlist_path = Path(arguments[1])
        with watchlist_path.open(encoding="utf-8", newline="") as source:
            entries = parse_watchlist(source)

        print(f"watchlist has {len(entries)} films")
        return 0

    print("letterbash: find the film that fits")
    return 0
