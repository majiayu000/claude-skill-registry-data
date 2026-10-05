---
name: review-shell
description: Use when reviewing, debugging, or hardening Shell/Bash scripts in this repo (.github/workflows/*.yml steps, website build scripts, or any *.sh file) or when asked to "review bash", "revisa el script", "shellcheck", or "revisa el pipeline shell". Reviews for robustness, error handling, quoting, portability, injection, and CI-friendliness, and ends with what a CI failure or a hostile input would catch.
---

# Shell / Bash Review

You review shell scripts like a sysadmin who has seen every broken pipe,
unquoted variable, and half-run pipeline. You assume any input can be hostile,
any command can fail, and anyone else running the script is using a different
shell on a different OS.

## Steps

1. **Read the whole script** before judging. Know what it is *for*.
2. **Lint mechanically first** — run `shellcheck` if available (each shell
   file), `bash -n file.sh` for syntax, `sh -n` for POSIX sh. Fix everything
   mechanical before the deep pass.
3. **Review the dimensions below.**
4. **Failure-thinking pass** — for each step, ask: *what happens if this
   command fails mid-way, if the input has spaces, or if a variable is empty?*
5. **Report** in the output format at the bottom.

## Review dimensions

1. **Set strict mode deliberately** — is `set -euo pipefail` present and
   understood? `set -e` surprises (failing in `if` conditions, in pipelines,
   with `grep` returning 1). Call out code that will die *or silently
   continue* under `set -e` in ways the author did not intend.
2. **Quoting** — every expansion quoted: `"$VAR"`, `"$@"`, `"${arr[@]}"`.
   Unquoted variables break on spaces/globs. This is the single most common
   real bug. Flag every unquoted expansion.
3. **`$@` vs `$*`** — use `"$@"` for argument lists, never `$*` or unquoted
   `$@`.
4. **Exit codes and error propagation** — every command that can fail is
   checked (`|| exit 1`, `if ! cmd; then`, `trap`). No `;`-chained commands
   where a failure would be silently swallowed.
5. **Injection and unsafe eval** — no `eval`, no `$(echo "$USER_INPUT")` in
   shell that runs commands, no `sh -c` from concatenated strings, no
   unchecked `find -exec`. Filenames/paths from input must be quoted and
   treated as data.
6. **Portability** — shebang matches usage (`#!/usr/bin/env bash` vs `sh`);
   no bashisms in `sh` scripts; no GNU-only flags (`find -regex` in a
   busybox-free environment is fine, but note `sed -i`, `head -n`, `xargs -I`
   portability); avoid `cd X && cmd` — prefer `(cd X && cmd)` subshells or
   `git -C`, and never mutate the caller's working directory.
7. **Cleanup and traps** — temp files removed (`trap 'rm -f "$tmp"' EXIT`),
   `trap ERR/EXIT/INT`, no leftover processes, no infinite loops without a
   guard.
8. **CI-friendliness (GitHub Actions especially)** — steps are idempotent,
   fail loudly (`|| exit 1`), don't depend on cwd or environment that isn't
   set, `$GITHUB_ENV`/`$GITHUB_OUTPUT` used instead of hidden file writes,
   secrets never echoed or written to logs.

## Failure-thinking checklist

- Empty variables, unset variables under `set -u`.
- Paths and filenames with spaces, quotes, or newlines.
- Commands that exit non-zero in `if`/`&&`/`||` chains.
- Partial runs (script killed at step N) — is state left behind?
- Re-runs — is the script idempotent, or does it double-apply?
- Environment differences (Windows CI, macOS, minimal containers).

## Output format

- **Verdict** — lint results, then pass/fail per dimension.
- **Issues** prioritized:
  - **Critical** — unquoted expansions in dangerous spots, injection,
    destructive commands (`rm -rf`) with unguarded variables, `set -e`
    swallowing a real failure.
  - **Important** — missing error checks, `cd` without subshell, unquoted
    variables, missing traps.
  - **Style** — readability, naming, comments.
  Each with `file:line`, the problem, and the fix as a code snippet.
- **Failure cases** — the 3-5 concrete scenarios (input or CI state) that
  would break the script, with the exact fix.
- When asked to fix, apply edits and re-run `shellcheck`/`bash -n` before
  reporting done.
