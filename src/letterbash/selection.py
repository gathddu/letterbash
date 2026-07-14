from collections.abc import Sequence
from random import Random, choice
from letterbash.watchlist import WatchlistEntry


def choose_film(
    candidates: Sequence[WatchlistEntry],
    *,
    rng: Random | None = None,
) -> WatchlistEntry:
    if not candidates:
        raise ValueError("can't choose a film from an empty watchlist")

    if rng is None:
        return choice(candidates)

    return rng.choice(candidates)
