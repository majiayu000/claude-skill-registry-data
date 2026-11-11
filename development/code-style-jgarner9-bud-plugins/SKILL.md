---
name: code-style
description: How Jason writes, tests, reviews and commits code. Go first, plus shell and Lua; small standard-library tools with a spec and tests; errors that say what to do next; safe defaults for anything that touches files, git or the network. Use whenever writing, changing, reviewing or refactoring code, writing tests, scripts, CLIs or config, or writing a commit message.
---

# Code style

The repo wins: its `CLAUDE.md`, formatter and linter config, and the code around the change come before anything here. These are the defaults when a repo doesn't say. Read the code before you assume a planned feature exists.

## Shape

- Small tools that each do one job. Standard library first: in Go, no third-party modules unless the repo already has them or Jason asks. CLIs use `flag` (one `flag.FlagSet` per subcommand), not a framework, and flags come before positionals.
- One source of truth per concern: build each path in one function, define each setting in one place, document each format in one file.
- Output is deterministic: the same input always gives the same output, sorted and stable.
- Config and data files are JSON. A tool that rewrites one keeps keys it doesn't know.
- Build what was asked. No speculative options, layers or abstractions.

## Errors and exit codes

- Functions return errors. Only the entry point prints them, as one `tool: message` line on stderr, and picks the exit code: 0 success, 1 failure, 2 bad usage.
- Wrap with what was being done, lowercase, no final period: `fmt.Errorf("read the report: %w", err)`.
- Say what to do next and what was kept: `can't find the default branch: set origin/HEAD with git remote set-head origin -a`, `nothing pushed (worktree kept at ...)`.
- A command that isn't built yet fails saying so. Never a silent exit 0.

## Anything that changes state

- Only touch what the tool created. Track managed files in a manifest: update the ones that are unchanged, delete the ones a release dropped, and leave everything else alone. When a managed file was edited by hand, skip it and say so.
- Write files that get rewritten atomically (temp file, then rename).
- Before a destructive step, list exactly what will happen and confirm on the terminal. Without a terminal, refuse and name the `--yes` flag. Add `--dry-run` where it's cheap.
- git: fast-forward only. Never force-push, never rewrite shared history, never merge on Jason's behalf. On divergence, stop and report.
- Never install or upgrade system packages silently. Report what's missing and the exact command to fix it.
- Secrets come from the environment or the OS keychain, never from the repo, logs or command-line arguments.
- Network work never blocks startup: run checks in the background and apply the result next time.

## Terminal output

- Color only when writing to a terminal, `TERM` isn't `dumb` and `NO_COLOR` is unset, so pipes and tests stay plain. Pad text before coloring it.
- Plain Unicode symbols, never emoji.
- Prompts read from the terminal (`/dev/tty` when stdin is a pipe, as under `curl | sh`). With `--yes` or no terminal, take the defaults.

## Tests

- Tests run with no network and no credentials: fake the external CLIs on `PATH` (a fake `claude`, `gh`, `git` remote), use real git in temp dirs, and point `HOME` and the XDG dirs at throwaway directories.
- Golden files for output, with an `-update` flag; review the diff before committing it.
- Name tests for the behavior, as a sentence: `TestChangesOutsideTheAllowedPathsAreNotPushed`.
- Go: swap package-level vars and restore them with `t.Cleanup`; helpers call `t.Helper()`; failure messages show what was expected and the context.
- A failing test blocks the install or release, never just warns.
- Bug fixes come with the test that would have caught them.

## Docs and comments

- Each tool has a `SPEC.md`: usage with a flag table, the behavior as numbered steps with each outcome, the output format, and how it's tested. Change the spec and the code together.
- A file or package header says what it does and what it never does. Other comments say why, not what.
- Commands in a README or `CLAUDE.md` are exact and copy-pasteable. When a check can keep docs honest (every config key documented), add it.

## Per language

- **Go:** gofmt and `go vet` clean. `main` is `os.Exit(cli(os.Args[1:], os.Stdout, os.Stderr))`, so the whole CLI runs in tests with buffers.
- **Shell:** shellcheck clean. Bash scripts start with `set -euo pipefail` (or `-uo` when they handle failures themselves) and indent with tabs. Anything piped to `sh`, like an installer, is POSIX `sh`. Scripts that run on macOS also work with its bash 3.2: no associative arrays, `mapfile` or `${x,,}`, and `shasum` where Linux has `sha256sum`.
- **Lua (Neovim):** stylua (2 spaces, double quotes, 120 columns) and selene. Modules build `local M = {}` and return it, with `---` doc comments.
- Target macOS and Linux unless the repo says otherwise.

## Commits

- Lowercase conventional commits with the issue id when there is one: `fix: skip dot entries in dev link (JGA-167)`. Types: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`.
- One commit per task, made once the project's checks pass (the repo's `just check` or CI command).

## Reviewing

Report, don't edit. Ranked worst first:

1. Bugs: wrong logic, off-by-one, nil or empty cases, error paths that are swallowed or leave things half done, races.
2. What the change misses: callers, docs or tests that needed updating.
3. Security: secrets in code or logs, unchecked input reaching a shell, a path or a query.
4. Fit: does it read like the code around it, and is anything more complicated than it needs to be?

For each finding give the file and line, what's wrong, a concrete case where it breaks, and the fix. Skip what a formatter would catch. If nothing is worth fixing, say so in one line.
