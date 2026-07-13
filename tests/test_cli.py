from letterbash.cli import main
import pytest


def test_main_introduces_letterbash(
    capsys: pytest.CaptureFixture[str],
) -> None:

    exit_code = main([])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "letterbash: find the film that fits\n"
    assert captured.err == ""
