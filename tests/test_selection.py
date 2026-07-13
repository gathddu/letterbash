from datetime import date

from letterbash.selection import choose_film
from letterbash.watchlist import WatchlistEntry


def test_choose_film_returns_the_only_candidate() -> None:
    candidate = WatchlistEntry(
        added_on=date(2023, 1, 4),
        name="Good Luck",
        year=2014,
        letterboxd_uri="https://boxd.it/7hJK",
    )

    assert choose_film([candidate]) == candidate
