# Letterbash

Letterbash is a terminal application that helps you choose a film from your watchlist.

An AI recommender might happen someday. Right now, I'm broke, my laptop is old and I'm tired, so Letterbash picks at random. Fate has no subscription fee.

## Commands

```
letterbash --help
letterbash import [PATH]
letterbash pick [PATH]
```

`PATH` is optional. When it's omitted, Letterbash checks `LETTERBASH_WATCHLIST`, then `$XDG_DATA_HOME/letterbash/watchlist.csv` and `~/.local/share/letterbash/watchlist.csv` when `XDG_DATA_HOME` is unset.

| File | Responsibility |
| ---- | -------------- |
| `src/letterbash/cli.py` | Command routing, terminal output, diagnostics  and process exit codes |
| `src/letterbash/watchlist.py` | Letterboxd CSV parsing and `WatchlistEntry` construction |
| `src/letterbash/selection.py` | Curent film selection and empty-candidate validation |
| `tests/test_cli.py` | Command-line acceptance contracts |
| `tests/test_watchlist.py` | Parser contracts and malformed-input behavior |
| `tests/test_selection.py` | Selection-domain contracts and deterministic random tests |
| `flake.nix` | Reproducible package and development-shell definitions |
| `pyproject.toml` | Python metadata, entry point, build system and tool configuration |

## To-Do

- [X] Create the Python package and terminal entry point
- [X] Parse Letterboxd watchlist exports
- [X] Support blank film years
- [X] Choose randomly with injectable randomness for deterministic tests
- [X] Add `import PATH` and `pick PATH`
- [X] Report empty and missing watchlists cleanly
- [X] Share watchlist loading across file reading commands
- [X] Reject unknown commands, missing paths and extra arguments
- [X] Add help and version output
- [X] Validate required columns, years and dates
- [X] Package Letterbash with Nix
- [X] Reject truncated or otherwise malformed CSV rows cleanly
- [X] Decide how blank required cell values should be handled
- [X] Add final packaged acceptance checks against the real export
- [X] Run `nix flake check` as part of the release gate
- [ ] Add a license
- [ ] Tag the first release
- [ ] Decide whether `import` remains a public command or is replaced by validation/status output
- [ ] Support a default watchlist path
- [ ] Store configuration in an XDG-compliant location
- [ ] Define an interactive reroll/accept workflow
- [ ] Add optional filters supported by available local data
- [ ] Add local history and optional immediate-repeat prevention
- [ ] Add continuous integration for formatting, linting, typing, tests and Nix builds
- [ ] Establish changelog, versioning and release procedures
- [ ] Verify supported Linux architectures in clean environments
- [ ] Add shell completions
- [ ] Add a manual page
- [ ] Consider structured output for scripts without compromising the default human-readable interface
- [ ] Add migration rules if configuration or history formats become persistent
- [ ] Evaluate support outside NixOS/Linux after the Linux release is stable
