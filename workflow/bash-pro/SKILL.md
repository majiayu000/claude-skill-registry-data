---
name: bash-pro
description: Bash scripting guidance — safe scripting patterns, quoting, error handling, pipes, and maintainable shell code.
category: development
---

## Overview

Bash is the glue of Unix systems: deployment scripts, CI steps, cron jobs, and one-liners that would take fifty lines in another language. It's also a footgun collection — unquoted variables, silent failures, and pipe errors have caused legendary outages. The difference is discipline: a few strict habits make bash scripts reliable instead of terrifying.

This skill covers the safe subset of bash: strict mode, quoting, error handling, and the patterns for writing scripts you'd trust in production — plus knowing when to reach for Python instead.

## When to use

- Writing shell scripts (deploy, backup, CI, automation).
- Debugging existing bash scripts.
- Choosing between bash and Python for a task.
- Writing safe one-liners and pipelines.
- Handling arguments, config, and logging in scripts.
- Making scripts idempotent and testable.

## Core concepts

- **Strict mode.** `set -euo pipefail` — exit on error, fail on undefined variables, propagate pipe failures. The single most important bash habit; without it, scripts fail silently and continue.
- **Quoting.** Always quote `"$variables"` — unquoted expansions undergo word splitting and globbing. The #1 source of "works until the filename has a space" bugs. Use `"$@"` for argument arrays.
- **Exit codes.** `0` success, non-zero failure; check explicitly where it matters (`if ! command; then`). `$?` captures the last status — use it immediately before anything overwrites it.
- **Pipes and pipefail.** `cmd1 | cmd2` — without `pipefail`, a failing `cmd1` is masked by `cmd2`'s success. `set -o pipefail` fixes it; still, avoid mega-pipes that are undebuggable — break complex logic into steps with temp files or variables.
- **Conditionals.** `[[ ]]` over `[ ]` (fewer surprises, pattern matching, no word splitting); `-f`/`-d`/`-n`/`-z` tests; `(( ))` for arithmetic. Quote inside `[[ ]]` only where needed — it's safer than `[ ]` by design.
- **Functions.** Named functions with `local` variables — `local` prevents global-namespace pollution, the source of subtle cross-function bugs. Return values via stdout or namerefs, not just exit codes.
- **Arguments.** `$1`, `$@`, `$#`; `getopts` for flags; validate argument counts and show usage. Scripts with undocumented arguments are write-only.
- **Error handling.** `trap` for cleanup (temp files, locks) on EXIT/ERR/INT — scripts must clean up after themselves even when interrupted.
- **Idempotency.** Scripts should be safe to re-run: check before creating (`mkdir -p`, `grep -q || append`), use locks (`flock`) for cron jobs that might overlap.
- **Here-docs and here-strings.** `<<EOF` for multiline input, `<<<` for single strings — cleaner than `echo` chains for generating config files.
- **Process substitution.** `<(cmd)` and `>(cmd)` — diffing command outputs, feeding pipelines as files. Powerful for comparisons without temp files.
- **Arrays.** `arr=(a b c)`, `"${arr[@]}"` — for lists that survive spaces. Associative arrays (`declare -A`) for key-value maps.
- **Debugging.** `set -x` traces execution; `bash -n` syntax-checks without running; ShellCheck (the linter) catches most bugs statically — run it in CI on every script.
- **When not bash.** Complex data structures, JSON/XML processing beyond `jq`, error handling with retries, anything over ~100 lines — that's Python's job. Bash for orchestration, Python for logic.
- **Portability.** `#!/usr/bin/env bash`, avoid bashisms in `sh` scripts, beware GNU vs BSD tool differences (macOS vs Linux `sed`/`date`).

## Practical workflow

1. **Start every script with the template.** Strict mode, usage function, main guard:
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   IFS=$'\n\t'

   usage() { echo "Usage: $(basename "$0") <env>"; exit 1; }
   [[ $# -eq 1 ]] || usage

   main() {
     local env="$1"
     # ... script logic ...
   }
   main "$@"
   ```
2. **Quote everything.** `"$var"`, `"$@"`, `"${arr[@]}"` — make unquoted expansion a code-review red flag.
3. **Handle errors explicitly.** Check critical commands; `trap` cleanup for temp files and locks:
   ```bash
   tmpdir=$(mktemp -d)
   trap 'rm -rf "$tmpdir"' EXIT INT TERM
   ```
4. **Use locks for scheduled scripts.** `flock` prevents overlapping cron runs from corrupting state:
   ```bash
   exec 9>/var/lock/myscript.lock
   flock -n 9 || { echo "Already running"; exit 0; }
   ```
5. **Log with timestamps.** Consistent log functions beat bare `echo`; log to stderr for diagnostics, stdout for data:
   ```bash
   log() { echo "[$(date '+%F %T')] $*" >&2; }
   ```
6. **Parse args with getopts.** Flags, defaults, validation — scripts grow options, plan for it:
   ```bash
   while getopts "e:v" opt; do
     case $opt in e) env="$OPTARG";; v) verbose=1;; *) usage;; esac
   done
   ```
7. **Lint with ShellCheck.** In CI and in the editor; treat warnings as errors for new scripts. It catches quoting, pipefail, and portability issues mechanically.
8. **Know when to switch.** Hitting arrays-of-associative-arrays, complex retries, or 150 lines? Rewrite in Python — bash's job was orchestration, and it's done.

## Common pitfalls

- **No `set -euo pipefail`** — silent failures continuing; strict mode always.
- **Unquoted variables** — word splitting and globbing; quote `"$var"` everywhere.
- **Parsing `ls`** — filenames with spaces/newlines break it; use globs or `find -print0`.
- **`cd` without checking** — `cd $dir; rm -rf *` in the wrong directory; `cd "$dir" || exit 1`.
- **Overwriting with `>`** — clobbering files accidentally; `set -o noclobber` in interactive shells, care in scripts.
- **Ignoring pipe failures** — `set -o pipefail` or explicit `${PIPESTATUS[@]}` checks.
- **Global variables in functions** — cross-function contamination; `local` everything.
- **No trap cleanup** — temp files and locks leaking on interrupt; trap EXIT/INT/TERM.
- **Overlapping cron runs** — no locking; `flock` for scheduled scripts.
- **Bash for complex logic** — 200-line scripts with nested JSON parsing; switch to Python.
- **Hardcoded paths** — `/tmp` races and assumptions; `mktemp`, configurable paths.
- **`echo` for data** — mixing diagnostics and output; log to stderr, data to stdout.
- **Assuming GNU tools** — macOS/BSD differences in `sed`, `date`, `stat`; test on target platforms or use portable constructs.
