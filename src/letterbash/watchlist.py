from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from typing import TextIO


@dataclass(frozen=True)
class WatchlistEntry:
    added_on: date
    name: str
    year: int | None
    letterboxd_uri: str


def parse_watchlist(source: TextIO) -> list[WatchlistEntry]:
    reader = csv.DictReader(source)
    required_columns = ("Date", "Name", "Year", "Letterboxd URI")
    fieldnames = reader.fieldnames or []
    missing_columns = [
        column for column in required_columns if column not in fieldnames
    ]
    if missing_columns:
        raise ValueError(f"missing required watchlist column: {missing_columns[0]}")

    entries: list[WatchlistEntry] = []

    for row in reader:
        missing_values = [column for column in required_columns if row[column] is None]
        if missing_values:
            raise ValueError(
                f"watchlist row {reader.line_num} is missing a value for: "
                f"{missing_values[0]}"
            )

        raw_year = row["Year"]
        try:
            year = int(raw_year) if raw_year else None
        except ValueError as error:
            raise ValueError(f"invalid watchlist year: {raw_year}") from error
        raw_date = row["Date"]
        try:
            added_on = date.fromisoformat(raw_date)
        except ValueError as error:
            raise ValueError(f"invalid watchlist date: {raw_date}") from error

        entries.append(
            WatchlistEntry(
                added_on=added_on,
                name=row["Name"],
                year=year,
                letterboxd_uri=row["Letterboxd URI"],
            )
        )

    return entries
