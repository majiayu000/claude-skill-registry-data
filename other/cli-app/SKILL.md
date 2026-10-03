---
name: cli-app
description: Conventions for command-line tools — argument/flag design, exit codes, stdout/stderr discipline, non-interactive behavior. Use when building or reviewing a CLI (any language), not a web/network-facing app.
---

# CLI app conventions

A CLI's "API" is its flags, exit codes, and output streams — scripts and CI
pipelines depend on all three, not just the happy-path behavior a human sees in a
terminal.

## Argument and flag design

- Support both long (`--verbose`) and short (`-v`) forms for common flags; a flag
  that only exists as `--extremely-descriptive-name` with no short form is fine for
  rare ones.
- `--help`/`-h` and `--version`/`-V` always work, need no other flags/args to be
  valid, and exit 0.
- Flags are additive and order-independent. Don't make behavior depend on flag
  order unless the tool is explicitly a pipeline (`cmd a | cmd b` style).
- Prefer explicit subcommands (`tool add`, `tool remove`) over one flag that
  changes what every other flag means.
- A destructive/irreversible action needs an explicit confirmation or a `--force`/
  `--yes` flag to skip it in scripts — never irreversible by default with no escape
  hatch for automation.

## Exit codes

- `0` = success. Non-zero = failure — scripts and CI depend on this to branch;
  never exit 0 after printing an error to make output "look clean."
- Distinguish usage error (bad flags/args, e.g. `2`) from a failure during
  execution (e.g. `1`) where the ecosystem convention supports it — a caller
  should be able to tell "you used me wrong" from "the operation failed."
- A caught signal (SIGINT/SIGTERM) exits with the conventional `128 + signal
  number` where the platform supports it, rather than swallowing it into exit 0/1.

## stdout vs. stderr

- Actual output/results go to stdout — the thing meant to be piped, redirected, or
  captured by a script.
- Progress messages, warnings, and logs go to stderr, so `cmd > out.txt` doesn't
  pollute the captured data with "Loading..." noise.
- Errors go to stderr with a non-zero exit, never printed to stdout with exit 0.

## Non-interactive / scripted use

- Detect non-interactive contexts (no tty, `CI` env var set) and disable behavior
  that assumes a human: prompts, spinners, colorized/ANSI output, interactive
  confirmation. Provide flags to force either mode explicitly
  (`--no-input`/`--yes`).
- Machine-readable output (`--json`, `--porcelain`) is a stable, documented format
  a script can parse — don't let it drift alongside the human-readable format
  without a version/compatibility note (see `api-design` skill's versioning
  section; the same discipline applies to a CLI's output shape).
- Respect `NO_COLOR` and non-tty stdout for disabling ANSI color automatically.

## Config and environment

- Precedence order is explicit and documented: flags override env vars override a
  config file override defaults — never silently let one clobber another with no
  way to tell which took effect.
- Config file location follows platform convention (XDG on Linux, `~/Library/...`
  on macOS, `%APPDATA%` on Windows) rather than a hardcoded dotfile in `$HOME`
  users can't predict.
