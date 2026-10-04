---
name: sota-shell-scripting
description: >-
  State-of-the-art shell scripting (bash and PowerShell, defensive) for writing and auditing shell scripts, CI scripts, init/deploy scripts, container entrypoints, and Makefile recipes — and equally for the ad-hoc commands you run yourself: a grep/find/rg sweep whose result you are about to report, a one-liner pasted from a checklist, a pipeline whose exit status or empty output you are about to believe. Use when creating, modifying, reviewing or hardening shell code, AND before trusting any conclusion a shell command produced — especially an ABSENCE ("no matches", "0 results"), which a quoting bug produces identically. Trigger keywords: bash, shell script, sh, zsh, shellcheck, shfmt, CI script, Makefile shell, entrypoint script, set -euo pipefail, dotfiles, install script, cron job, wrapper script, one-liner, command line, grep sweep, search the codebase, verify a claim, no matches found, empty output, exit status, word splitting, glob, PowerShell, pwsh, .ps1, Windows CI, ErrorActionPreference.
---

# SOTA Shell Scripting

Purpose: produce shell scripts that survive contact with reality — unusual filenames, missing
commands, partial failures, hostile input, signals, and concurrent invocation — and audit
existing scripts for the defect classes that cause most production shell incidents:
unquoted expansions, silent error swallowing, injection, secret leakage, and temp-file races.

Bash-focused (written for bash 5.x; macOS ships bash 3.2 and defaults to zsh — see portability
rules). POSIX `sh` only when the target demands it (busybox/dash containers, init systems).

## First decision: should this be shell at all?

**Do NOT use shell when any of these hold.** Recommend Python/Go (or the project's primary
language) instead, and say so explicitly in BUILD and AUDIT output:

- Script exceeds ~100 lines of actual logic (not counting boilerplate/usage text).
- Needs real data structures (nested maps, JSON manipulation beyond a `jq` one-liner, sets).
- Needs granular error handling (retry *this* step, distinguish error kinds, partial rollback).
- Does arithmetic beyond integers, date math, or float comparison.
- Parses structured formats (JSON/YAML/XML) with string surgery instead of `jq`/`yq`.
- Needs portable concurrency beyond "run N jobs and `wait`".
- Is security-critical input handling (auth, parsing untrusted network data).

Shell is the right tool for: gluing processes together, CI steps, container entrypoints,
small install/deploy wrappers, environment setup — anything that is mostly *invoking other
programs* rather than computing.

## BUILD mode

When writing or modifying shell scripts:

1. **Pick the dialect deliberately.** `#!/usr/bin/env bash` unless the target is a minimal
   container/init context that only guarantees POSIX `sh`. Never `#!/bin/sh` with bashisms.
2. **Start every bash script from the safety preamble** (rules/01): `set -euo pipefail`,
   trap-based cleanup, `IFS` discipline — and know where `set -e` does NOT fire.
3. **Quote every expansion.** `"$var"`, `"$@"`, `"$(cmd)"`. Build commands with arrays,
   never with string concatenation.
4. **Errors are loud and routed to stderr** with script name + context; exit codes are
   meaningful and documented in `--help`.
5. **Make it idempotent and interrupt-safe**: `mktemp` + `trap` cleanup, atomic writes via
   `mv`, check-before-create, `flock` if concurrent runs are possible.
6. **Run `shellcheck` (treat all findings as blockers, suppress only with a justifying
   comment) and `shfmt -d` before declaring done.** If they are unavailable locally, state
   that and flag CI must run them.
7. Provide `--help` always; `--version` for distributed tools; `set -x` behind a
   `DEBUG`/`TRACE` env guard, never unconditionally (secret leakage).

## AUDIT mode

When reviewing existing shell scripts, hunt the defect classes in rules/ files bottom-up
(each rules file ends with an audit checklist of grep patterns and ShellCheck codes).
Run `shellcheck -S style` on every script if available; correlate findings with context —
ShellCheck flags symptoms, you judge exploitability and blast radius.

Severity conventions:

| Severity | Meaning | Examples |
|---|---|---|
| CRITICAL | Exploitable or data-destroying now | `eval` on untrusted input; unquoted var in `rm -rf`; secrets in argv/`set -x`; curl\|bash of unpinned URL in prod |
| HIGH | Will corrupt/fail on realistic input or failure | unquoted expansions in destructive paths; missing `set -e`/error checks around critical steps; predictable temp files; non-atomic config writes; missing `exec` in entrypoint (signals lost) |
| MEDIUM | Latent bug or fragility | parsing `ls`; `which` instead of `command -v`; missing `pipefail`; no `--` separators; no timeouts on network calls; `echo` for variable data |
| LOW | Style/maintainability with safety implications | missing `local`; `[ ]` where `[[ ]]` intended; missing `readonly`; inconsistent error messages |

Finding format:

```
[SEVERITY] file:line — short title (SCxxxx if applicable)
  Evidence: the offending line(s), verbatim
  Impact: what input/condition triggers it and what breaks
  Fix: concrete replacement code
  Effort: trivial | small | medium | large
```

## Rules index

| File | Covers |
|---|---|
| [rules/01-safety-baseline.md](rules/01-safety-baseline.md) | Shebang discipline, `set -euo pipefail` and its real limitations, quoting & word-splitting bug catalog, **zsh-vs-bash deviations that bite pasted commands (joining, `pipestatus`, and `NOMATCH` — an unquoted glob in a flag value aborts the command and fakes a clean sweep)** |
| [rules/07-powershell.md](rules/07-powershell.md) | **PowerShell has no `set -euo pipefail`, and the line everyone omits is the one that matters: `$PSNativeCommandUseErrorActionPreference` defaults to `$false`, so `$ErrorActionPreference = 'Stop'` silently tolerates a failed `git`/`docker`/`terraform` (§1)** · The same failure classes as bash with different mechanisms: three disagreeing status variables and a `$?` that does not climb out of a function, `pwsh -Command` letting the **last statement** decide a CI step's verdict, GitHub Actions' built-in shell being safe while a custom `shell:` string silently drops its fail-fast and exit propagation, `Invoke-Expression` as `eval`, execution policy as the control that is **not** a security boundary, and PSScriptAnalyzer where ShellCheck cannot reach |
| [rules/06-ad-hoc-commands.md](rules/06-ad-hoc-commands.md) | **`rg -r` is `--replace`, not recursive — the `grep -r` symlink trap inverted, fabricating false CONTENT instead of a false absence (§2a)** · The commands nobody commits — a sweep, a probe, a one-liner from a checklist, a quick container copy: the zsh deviations that bite pasted commands (joining, `pipestatus`, `NOMATCH` faking a clean sweep, **a pipe into `python3 - <<EOF`** that bash discards and zsh runs as code), **what your searcher silently excludes** (`-r` vs symlinked dirs, ripgrep's gitignore defaults, a `grep` that is really a wrapper) and controlling a sweep in the same invocation, **a pattern beginning with `-` parsed as a flag** (clean zero, error on the stderr you suppressed, §2c), **`|| echo "missing X"` firing on *any* non-zero exit** so your broken sweep is reported as their defect (§2d), **a hardcoded label asserting the result the output above it contradicts** (§2e), and **a backslash escape (`\b`, `\s`, `\w`, `\d`) that is a property of the machine rather than the tool** — `\b` silently matches nothing where `git grep` inherits a BSD regex (§2f) |
| [rules/09-listing-and-selection.md](rules/09-listing-and-selection.md) | **A lister's default cap answers with exit 0 and an empty stderr, so a page reads as a population (§5)** · The tools that *enumerate* rather than search: `gh pr list` returning 30 of 330 with no flag and no warning, the `--limit` you set for a different question and then counted with, server-side counts and `--paginate` as the fix, reconciling two methods that disagree to a named cause — and **the selector that picked a neighbouring population** (§5a): *newest* is not *default*, apparent size is not blocks freed, and the only tell is a value that cannot belong to the thing you asked about — and **the filter that drops the file you named** (§5b): an `--include='*.rb'` filter beside a named `config.ru` means grep never reads `config.ru` on BSD, ugrep or GNU, so the probe exits 1 like a clean codebase |
| [rules/08-ad-hoc-side-effects.md](rules/08-ad-hoc-side-effects.md) | **"I am only checking something" bounds nothing — a read-only *intent* is not a read-only *command*** · The sibling of rules/06: that file is a check returning the wrong answer, this one is a check with **side effects**. An ad-hoc command that fills a disk or corrupts the runtime it was inspecting (§3), and a backgrounded wait loop that exhausts the **process table** (§4) — which does not degrade, it hits a ceiling where every tool fails at once, *including cleanup*, since `ps`, `killall` and even `echo` in a fresh shell all need to fork |
| [rules/05-constructs-and-cleanup.md](rules/05-constructs-and-cleanup.md) | **Sourcing a script to test one function relocates it — `BASH_SOURCE` points at the copy and the script `cd`s itself away, silently (§3a)** · The constructs a script is assembled from, once the expansion itself is right: arrays for command building (SC2089/2090), IFS scoping, `trap`-based cleanup and `mktemp` (predictable temp paths are a race, not a style point; an ERR trap without `set -E` is silent inside functions), `[[ ]]`/printf/`local`/`readonly`, and globbing pitfalls including never parsing `ls`; **rewriting a script while it runs changes what it runs (§3d)** |
| [rules/02-robustness-correctness.md](rules/02-robustness-correctness.md) | Argument parsing (getopts/while-case, --help/--version), input validation, POSIX vs bash portability, stderr/exit-code discipline, PIPESTATUS, command -v, network timeouts & retries, flock & background jobs, idempotency & atomic writes, safe filename handling; **a `grep -c` count inside `$( )` aborts silently on zero under `set -e`** |
| [rules/03-security.md](rules/03-security.md) | **Why `--severity=style` catches real defects, and a pointer to who owns local gate reproduction (§7)** · eval/injection, secrets discipline (argv/env/set -x), PATH hygiene — including **the non-adversarial mirror: a wrapper, shim, alias or function override that invokes a name its own namespace shadows**, which fills the process table with no bound at all while the function form merely segfaults — sudo discipline, curl\|bash both directions, temp-file races, umask, ShellCheck+shfmt in CI |
| [rules/04-ci-and-operational.md](rules/04-ci-and-operational.md) | **Killing a backgrounded build by pid orphans the compiler, and the next run's contention reads as a defect in your change** · GitHub Actions shell pitfalls (`${{ }}` injection, multiline run, quoting in YAML), container entrypoints (exec, PID 1, privilege drop), Makefile shell gotchas, long-running script logging |

## Top 10 non-negotiables

1. `#!/usr/bin/env bash` + `set -euo pipefail` on every bash script — and explicit error
   handling where `-e` is known not to fire (conditions, `&&`/`||`, command substitution
   in assignments-with-modifiers, process substitution).
2. Quote **every** expansion: `"$var"`, `"$@"`, `"${arr[@]}"`, `"$(cmd)"`. SC2086 is a
   bug, not style.
3. Build argument lists with arrays; pass them as `"${args[@]}"`. Never accumulate a
   command in a string and `eval`/word-split it.
4. `trap cleanup EXIT` with an idempotent cleanup function; temp paths only via `mktemp`.
5. Never `eval`, `bash -c`, or `sh -c` with interpolated untrusted data; use `--` before
   positional file/user arguments to every command that supports it.
6. No secrets in argv, in environment dumps, or under `set -x` — **including `sh -x script`
   run to debug it**, which traces even `[ -n "$KEY" ]`; `set +x` around sensitive
   sections; read secrets from files or fds.
7. Errors to stderr with context (`script: failed to X: $detail`); meaningful exit codes;
   never `exit 0` on failure paths.
8. Network calls get `--fail`, `--max-time`/timeouts, and bounded retries — never bare
   `curl url | ...`.
9. Handle arbitrary filenames: `find -print0 | xargs -0` / `-exec ... +`, `while IFS= read -r`,
   never iterate `$(ls)` or unquoted globs from variables.
10. ShellCheck (clean, or annotated suppressions) + shfmt enforced in CI; a shell script
    without CI linting is unreviewed code.

## Cross-references

- CI pipeline hardening, `${{ }}` injection, action pinning → `sota-devsecops`
- Secret storage/rotation → `sota-secrets-management`
- Container image/runtime hardening → `sota-sandboxing`, `sota-cloud-infrastructure`
- When the "don't use shell" rule fires → `sota-python` / `sota-golang`
