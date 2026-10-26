---
name: bash
description: Use when writing or reviewing Bash scripts — deployment scripts, git hooks, scheduled jobs (cron or systemd timers), wrappers around CLIs, and glue between tools. Covers strict mode, quoting, locking against concurrent runs, idempotency, retries, safe temporary files and ShellCheck. Also use when a script works interactively but fails from a timer, a hook or CI.
---

# Bash

Default: `#!/usr/bin/env bash`, `set -euo pipefail`, ShellCheck clean, functions over long straight-line scripts, and a move to Python once logic needs data structures.

## Script skeleton

```bash
#!/usr/bin/env bash
set -euo pipefail
usage() { echo "usage: ${0##*/} [--dry-run] <target>" >&2; exit 2; }
dry=0
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run) dry=1 ;;
    -h|--help) usage ;;
    *) target=$1 ;;
  esac
  shift
done
[[ -n ${target:-} ]] || usage
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
```

## Rules that prevent most bugs

- Quote every expansion: `"$var"`, `"${arr[@]}"`. Unquoted variables split on spaces and expand globs.
- Use `[[ ... ]]` for tests and `$(...)` for command substitution.
- `set -e` does not fire inside `if` conditions, `&&`/`||` chains or command substitutions in some contexts; check critical commands explicitly.
- `pipefail` makes a pipeline fail if any stage fails — but `grep` returning 1 on "no match" then becomes an error; handle it (`grep ... || true`).
- Read files line by line with `while IFS= read -r line; do ...; done < file`.

## Running safely and repeatedly

- **One instance at a time:** `exec 9>"$lockfile"; flock -n 9 || { echo "already running" >&2; exit 0; }`.
- **Idempotent:** check state before changing it (does the branch exist, is the file already current) so a rerun after a failure is safe.
- **Write atomically:** write to a temp file in the same directory and `mv` it into place.
- **Retries:** loop with a cap and growing sleep for network commands; never retry forever.
- **Dry run first** for anything destructive, and print exactly what would happen.

## Timers, hooks and CI

- Timers and hooks run with a minimal environment: no interactive profile, a short `PATH`, a different working directory. Use absolute paths and set `PATH` at the top.
- Log with timestamps to a file or the journal (`logger -t name`), since nobody watches the terminal.
- In git hooks, read the message file passed as `$1`, do not assume the working directory, and chain to any pre-existing hook instead of replacing it.

## Verification loop

1. `shellcheck script.sh` — zero findings, or each suppressed with a reason.
2. `bash -n script.sh` for syntax.
3. Run with `--dry-run`, then for real, then run it again to prove idempotency.

## Pitfalls

- `cd` in a script without `|| exit` continues in the wrong directory.
- `rm -rf "$dir/"*` with an empty `$dir` targets `/`; guard with `${dir:?}`.
- `local var=$(cmd)` hides `cmd`'s exit status; declare and assign separately.
- `echo` interprets options and escapes inconsistently; use `printf '%s\n'`.
- Arithmetic with leading zeros (`08`) is treated as octal; force base 10 with `10#$n`.
- `sed -i` differs between GNU and BSD; on macOS use `sed -i ''` or prefer Python for edits.
