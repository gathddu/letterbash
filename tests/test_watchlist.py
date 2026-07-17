from datetime import date
from io import StringIO

from letterbash.watchlist import WatchlistEntry, parse_watchlist
import pytest


def test_parse_watchlist_reads_an_export_row() -> None:
    export = StringIO(
        "Date,Name,Year,Letterboxd URI\n"
        "2023-01-04,Good Luck,2014,https://boxd.it/7hJK\n"
    )

    assert parse_watchlist(export) == [
        WatchlistEntry(
            added_on=date(2023, 1, 4),
            name="Good Luck",
            year=2014,
            letterboxd_uri="https://boxd.it/7hJK",
        )
    ]


def test_parse_watchlist_reads_a_row_without_a_year() -> None:
    source = StringIO(
        "Date,Name,Year,Letterboxd URI\n"
        "2025-02-03,Unknown Film,,https://boxd.it/example\n"
    )

    entries = parse_watchlist(source)

    assert entries == [
        WatchlistEntry(
            added_on=date(2025, 2, 3),
            name="Unknown Film",
            year=None,
            letterboxd_uri="https://boxd.it/example",
        )
    ]


def test_parse_watchlist_rejects_a_missing_required_column() -> None:
    source = StringIO("Date,Name,Year\n2026-07-14,Film,2024\n")

    with pytest.raises(
        ValueError,
        match="^missing required watchlist column: Letterboxd URI$",
    ):
        parse_watchlist(source)


def test_parse_watchlist_rejects_an_invalid_year() -> None:
    source = StringIO(
        "Date,Name,Year,Letterboxd URI\n"
        "2026-07-14,Film,unknown,https://letterboxd.com/film/example/\n"
    )

    with pytest.raises(
        ValueError,
        match="^invalid watchlist year: unknown$",
    ):
        parse_watchlist(source)
