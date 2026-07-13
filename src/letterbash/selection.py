from collections.abc import Sequence
from random import Random, choice
from letterbash.watchlist import WatchlistEntry


def choose_film(
    candidates: Sequence[WatchlistEntry],
    *,
    rng: Random | None = None,
) -> WatchlistEntry:
    if rng is None:
        return choice(candidates)

    return rng.choice(candidates)
