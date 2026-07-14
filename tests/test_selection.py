from datetime import date
from random import Random

from letterbash.selection import choose_film
from letterbash.watchlist import WatchlistEntry

import pytest


def test_choose_film_returns_the_only_candidate() -> None:
    candidate = WatchlistEntry(
        added_on=date(2023, 1, 4),
        name="Good Luck",
        year=2014,
        letterboxd_uri="https://boxd.it/7hJK",
    )

    assert choose_film([candidate]) == candidate


def test_choose_film_can_select_among_multiple_candidates() -> None:
    first = WatchlistEntry(
        added_on=date(2023, 1, 4),
        name="Good Luck",
        year=2014,
        letterboxd_uri="https://boxd.it/7hJK",
    )

    second = WatchlistEntry(
        added_on=date(2024, 1, 27),
        name="Anatomy of a Fall",
        year=2023,
        letterboxd_uri="https://boxd.it/yuDE",
    )

    selected = choose_film([first, second], rng=Random(0))

    assert selected == second


def test_choose_film_rejects_an_empty_watchlist() -> None:
    with pytest.raises(
        ValueError,
        match="can't choose a film from an empty watchlist",
    ):
        choose_film([])
