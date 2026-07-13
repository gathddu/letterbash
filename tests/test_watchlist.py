from datetime import date
from io import StringIO

from letterbash.watchlist import WatchlistEntry, parse_watchlist


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
