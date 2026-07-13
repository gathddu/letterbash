from collections.abc import Sequence

from letterbash.watchlist import WatchlistEntry


def choose_film(candidates: Sequence[WatchlistEntry]) -> WatchlistEntry:
    return candidates[0]
