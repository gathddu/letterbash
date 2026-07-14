from letterbash.cli import main
import pytest
from pathlib import Path


def test_main_introduces_letterbash(
    capsys: pytest.CaptureFixture[str],
) -> None:

    exit_code = main([])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "letterbash: find the film that fits\n"
    assert captured.err == ""


def test_main_reports_watchlist_count(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:

    watchlist = tmp_path / "watchlist.csv"
    watchlist.write_text(
        "Date,Name,Year,Letterboxd URI\n"
        "2023-01-04,Good Luck,2014,https://boxd.it/7hJK\n"
        "2024-01-27,Anatomy of a Fall,2023,https://boxd.it/yuDE\n",
        encoding="utf-8",
    )

    exit_code = main(["import", str(watchlist)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "watchlist has 2 films\n"
    assert captured.err == ""


def test_main_picks_a_film_from_watchlist(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    watchlist = tmp_path / "watchlist.csv"
    watchlist.write_text(
        "Date,Name,Year,Letterboxd URI\n"
        "2023-01-04,Good Luck,2014,https://boxd.it/7hJK\n",
        encoding="utf-8",
    )

    exit_code = main(["pick", str(watchlist)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "Good Luck (2014)\n"


def test_main_reports_an_empty_watchlist(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    watchlist = tmp_path / "watchlist.csv"
    watchlist.write_text(
        "Date,Name,Year,Letterboxd URI\n",
        encoding="utf-8",
    )

    exit_code = main(["pick", str(watchlist)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == "letterbash: can't choose a film from an empty watchlist\n"


@pytest.mark.parametrize("command", ["import", "pick"])
def test_main_reports_a_missing_watchlist(
    command: str,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    watchlist = tmp_path / "missing.csv"

    exit_code = main([command, str(watchlist)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == f"letterbash: watchlist not found: {watchlist}\n"
