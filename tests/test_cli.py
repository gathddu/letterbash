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


def test_main_picks_a_film_without_a_year(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    watchlist = tmp_path / "watchlist.csv"
    watchlist.write_text(
        "Date,Name,Year,Letterboxd URI\n"
        "2026-07-14,Film Without a Year,,https://letterboxd.com/film/no-year/\n",
        encoding="utf-8",
    )

    exit_code = main(["pick", str(watchlist)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "Film Without a Year\n"
    assert captured.err == ""


def test_main_rejects_an_unknown_command(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main(["surprise"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert captured.out == ""
    assert captured.err == "letterbash: unknown command: surprise\n"


@pytest.mark.parametrize("command", ["import", "pick"])
def test_main_rejects_a_command_without_a_watchlist_path(
    command: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.delenv("LETTERBASH_WATCHLIS", raising=False)
    exit_code = main([command])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert captured.out == ""
    assert captured.err == f"letterbash: {command} requires a watchlist path\n"


@pytest.mark.parametrize("command", ["import", "pick"])
def test_main_rejects_extra_command_arguments(
    command: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main([command, "watchlist.csv", "extra"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert captured.out == ""
    assert captured.err == f"letterbash: {command} accepts only one watchlist path\n"


@pytest.mark.parametrize("option", ["--help", "-h"])
def test_main_prints_help(
    option: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main([option])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == (
        "usage: letterbash COMMAND PATH\n"
        "\n"
        "Choose a film from a Letterboxd watchlist export.\n"
        "\n"
        "commands:\n"
        "  import PATH  show the number of films in the watchlist\n"
        "  pick PATH    choose a film at random\n"
    )
    assert captured.err == ""


def test_main_prints_version(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("importlib.metadata.version", lambda _: "0.1.0")

    exit_code = main(["--version"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "letterbash 0.1.0\n"
    assert captured.err == ""


@pytest.mark.parametrize("command", ["import", "pick"])
def test_main_reports_a_watchlist_with_a_missing_required_column(
    command: str,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    watchlist = tmp_path / "watchlist.csv"
    watchlist.write_text(
        "Date,Name,Year\n2026-07-14,Film,2024\n",
        encoding="utf-8",
    )

    exit_code = main([command, str(watchlist)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == (
        "letterbash: missing required watchlist column: Letterboxd URI\n"
    )


@pytest.mark.parametrize("command", ["import", "pick"])
def test_main_reports_a_watchlist_path_that_is_a_directory(
    command: str,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main([command, str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == f"letterbash: watchlist is not a file: {tmp_path}\n"


@pytest.mark.parametrize("command", ["import", "pick"])
def test_main_reports_a_permission_denied_watchlist(
    command: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    watchlist = tmp_path / "watchlist.csv"

    def deny_access(*_: object, **__: object) -> None:
        raise PermissionError

    monkeypatch.setattr(Path, "open", deny_access)

    exit_code = main([command, str(watchlist)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == (
        f"letterbash: permission denied reading watchlist: {watchlist}\n"
    )


@pytest.mark.parametrize("command", ["import", "pick"])
def test_main_reports_a_non_utf8_watchlist(
    command: str,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    watchlist = tmp_path / "watchlist.csv"
    watchlist.write_bytes(
        b"Date,Name,Year,Letterboxd URI\n"
        b"2026-07-14,Film\xff,2024,https://letterboxd.com/film/example/\n"
    )

    exit_code = main([command, str(watchlist)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == (f"letterbash: watchlist is not valid UTF-8: {watchlist}\n")


@pytest.mark.parametrize(
    ("command", "expected_output"),
    [
        ("import", "watchlist has 1 films\n"),
        ("pick", "Film (2024)\n"),
    ],
)
def test_main_accepts_a_utf8_bom_watchlist(
    command: str,
    expected_output: str,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    watchlist = tmp_path / "watchlist.csv"
    watchlist.write_bytes(
        b"\xef\xbb\xbfDate,Name,Year,Letterboxd URI\n"
        b"2026-07-14,Film,2024,https://letterboxd.com/film/example/\n"
    )

    exit_code = main([command, str(watchlist)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == expected_output
    assert captured.err == ""


@pytest.mark.parametrize(
    ("command", "expected_output"),
    [
        ("import", "watchlist has 1 films\n"),
        ("pick", "Film (2024)\n"),
    ],
)
def test_main_uses_the_configured_watchlist_when_path_is_omitted(
    command: str,
    expected_output: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    watchlist = tmp_path / "watchlist.csv"
    watchlist.write_text(
        "Date,Name,Year,Letterboxd URI\n"
        "2026-07-14,Film,2024,https://letterboxd.com/film/example/\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("LETTERBASH_WATCHLIST", str(watchlist))

    exit_code = main([command])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == expected_output
    assert captured.err == ""
