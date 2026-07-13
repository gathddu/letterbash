from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from typing import TextIO


@dataclass(frozen=True)
class WatchlistEntry:
    added_on: date
    name: str
    year: int
    letterboxd_uri: str


def parse_watchlist(source: TextIO) -> list[WatchlistEntry]:
    reader = csv.DictReader(source)
    entries: list[WatchlistEntry] = []

    for row in reader:
        entries.append(
            WatchlistEntry(
                added_on=date.fromisoformat(row["Date"]),
                name=row["Name"],
                year=int(row["Year"]),
                letterboxd_uri=row["Letterboxd URI"],
            )
        )

    return entries
