---
name: forge-cli
description: "Forge: CLIs and dev tools: CLI, command line, argparse, flag, --help, exit code, stdin, stdout, pipe, dry-run, cross-platform, terminal, subcommand."
---

# Forge playbook — Command-line tool / CLI

**Do not duplicate ECC skills — defer to:** the language reviewer skills (`python-reviewer`, `typescript-reviewer`, `go-review`, `rust-review`, etc. by stack) for idiomatic code, and `/test-coverage` for the test gate. This file is orchestration only.

A CLI is a **contract with other programs, not just humans.** It is invoked by scripts, pipelines, CI, and other tools — so its arg surface, exit codes, and stdio behavior are the real API. `build-boss` implements; `test-boss` drives the exit-code + pipe integration tests; `docs-boss` produces the `--help`/usage/README. Never claim "cross-platform" for an OS you did not actually run on (see honest limit).

## Hard rules (non-negotiable)
- **Real arg parser + `--help` + `--version`.** Use the stack's established parser (argparse/click, commander/yargs, clap, cobra) — not hand-rolled `argv` slicing. `--help` and `--version` always work and exit `0`; usage is clear and shows at least one example; unknown flags fail with a helpful message, not a stack trace.
- **Correct exit codes.** `0` = success only; distinct non-zero codes for distinct failure classes (usage error, not-found, permission, runtime). **Never exit `0` on failure** — pipelines and CI branch on the exit code. Document the code table.
- **Pipe / stdio discipline.** Machine output → **stdout**; diagnostics, logs, prompts, progress → **stderr** (so `cmd | other` stays clean). Read **stdin** when piped / when the input arg is `-`. Offer a `--json` (or `--quiet`) mode for scripting. Respect non-TTY and `NO_COLOR`: no colors, spinners, or interactive prompts when output is piped or `stdin` is not a terminal. Don't crash on `SIGPIPE`/broken pipe (`head` closing early is normal).
- **No destructive default.** Any irreversible action (delete, overwrite, force-push, truncate, mass-rename) is NEVER the default: require an explicit flag or an interactive confirmation, offer `--dry-run` to preview, and gate override behind `--force`/`--yes`. A bare invocation must be safe.
- **Testable — I/O separated from logic.** Core behavior lives in pure functions callable without spawning a process; the thin CLI layer wires args → core → streams. Ship real tests that assert **exit codes, stdout, stderr, and pipe round-trips** (not just one happy path).
- **Cross-platform.** Use the platform path API (no hardcoded `/` or `\`), tolerate CRLF/LF, don't assume a POSIX-only shell or GNU-only flags, and handle Ctrl-C (SIGINT) cleanly. Secrets/tokens come from env or a config file — never echoed to stdout/stderr or baked into the binary.

## Team (conditional)
Lead: `architect` for a multi-subcommand tool, else `build-boss` directly. Implementation: **`build-boss`**. Review: `python-reviewer` / `typescript-reviewer` / the stack's reviewer (idiomatic parsing + error handling), `silent-failure-hunter` (a command that swallows an error and still exits `0` is the classic CLI bug). Tests: **`test-boss`** (exit-code + stdout/stderr + pipe integration). Docs: **`docs-boss`** (`--help` text, usage examples, man page/README, exit-code table). Optional advisor: `security-boss` when the tool shells out, handles secrets, or takes untrusted paths (command-injection / path-traversal).

## Skills / commands / MCP
Stack reviewer skill + `/test-coverage`; the parser library's own docs (Context7 / vendor) for exact flag/subcommand API. No special MCP needed. **Opt-in dependency:** genuine cross-platform verification needs a CI matrix (Windows + macOS + Linux runners) or local VMs — Forge writes portable code and tests, but a single dev box can only *run* the OS it is on; treat other-OS results as inferred until a matrix run proves them.

## Fan-out & flow
L1 for a single-purpose tool; L2 for a multi-subcommand CLI.
**Serial:** arg contract (flags + `--help` + exit-code table) → core logic (I/O-separated, pure) → stdio/pipe behavior → destructive-action guards → tests.
**Parallel (independent once the arg contract + shared core lib are fixed):** individual subcommands ∥ the help/usage docs ∥ the test suite.

## Domain gates
- `--help` and `--version` work and exit `0`; unknown flags fail cleanly with usage.
- Exit codes are distinct and correct; no path exits `0` on error (proven by a failing-input test).
- Machine output on stdout, diagnostics on stderr; reads stdin when piped; a pipeline `producer | tool | consumer` round-trips without leaking logs into the data stream.
- No destructive default: dry-run/confirm/force present and tested; a bare run is non-destructive.
- Cross-platform path + line-ending handling; no unguarded POSIX-only/GNU-only assumption; clean SIGINT.
- Tests cover exit codes + stdout + stderr + pipe; core logic is unit-testable without a subprocess.

## Ship-readiness (unique)
`--help`/`--version` verified; exit-code table documented AND tested (including a deliberate error path that returns non-zero); pipe round-trip proven (`echo ... | tool | tool`); destructive operations gated behind flag/confirm with a working `--dry-run`; runs on the declared target OSes (state which were actually run vs inferred); no secrets echoed to stdout/stderr; test suite green. Advisory checklist — optionally run `codex-reviewer` on the arg-dispatch + destructive-path code; not a blocker, but if a target OS was not actually run, say so.
