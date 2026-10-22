---
name: create-cli
description: >-
  Designs a command-line interface's surface: argument syntax, flags, help text, output formats, error
  messages, config handling, and dry-run behavior, following clig.dev. Use when creating a new CLI or
  reviewing one for human-friendliness and script compatibility.
source: "https://github.com/steipete/agent-scripts"
attribution: "steipete/agent-scripts by Peter Steinberger"
version: "1.0.0"
license: MIT
---

# Create CLI

> **Attribution:** Sourced from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) by [Peter Steinberger](https://github.com/steipete).

## When to Use

- Designing CLI argument syntax, flags, help text, and output format
- Reviewing CLI UX for human-friendliness and script-compatibility
- Specifying error messages, config handling, and dry-run behavior
- Creating a new command-line tool from scratch

Design CLI surface area (syntax + behavior), human-first, script-friendly.

Reference: https://clig.dev/

## Clarify (fast)

Ask, then proceed with best-guess defaults if user is unsure:

- Command name + one-sentence purpose.
- Primary user: humans, scripts, or both.
- Input sources: args vs stdin; files vs URLs; secrets (never via flags).
- Output contract: human text, `--json`, `--plain`, exit codes.
- Interactivity: prompts allowed? need `--no-input`? confirmations for destructive ops?
- Config model: flags/env/config-file; precedence; XDG vs repo-local.
- Platform/runtime constraints: macOS/Linux/Windows; single binary vs runtime.

## Deliverables

When designing a CLI, produce a compact spec the user can implement:

- Command tree + USAGE synopsis.
- Args/flags table (types, defaults, required/optional, examples).
- Subcommand semantics (what each does; idempotence; state changes).
- Output rules: stdout vs stderr; TTY detection; `--json`/`--plain`; `--quiet`/`--verbose`.
- Error + exit code map (top failure modes).
- Safety rules: `--dry-run`, confirmations, `--force`, `--no-input`.
- Config/env rules + precedence (flags > env > project config > user config > system).
- Shell completion story (if relevant): install/discoverability; generation command or bundled scripts.
- 5–10 example invocations (common flows; include piped/stdin examples).

## Default Conventions

- `-h/--help` always shows help and ignores other args.
- `--version` prints version to stdout.
- Primary data to stdout; diagnostics/errors to stderr.
- Add `--json` for machine output; consider `--plain` for stable line-based text.
- Prompts only when stdin is a TTY; `--no-input` disables prompts.
- Destructive operations: interactive confirmation + non-interactive requires `--force` or explicit `--confirm=...`.
- Respect `NO_COLOR`, `TERM=dumb`; provide `--no-color`.
- Handle Ctrl-C: exit fast; bounded cleanup; be crash-only when possible.

## CLI Spec Skeleton

Fill these sections, drop anything irrelevant:

1. **Name**: `mycmd`
2. **One-liner**: `...`
3. **USAGE**:
   - `mycmd [global flags] <subcommand> [args]`
4. **Subcommands**:
   - `mycmd init ...`
   - `mycmd run ...`
5. **Global flags**:
   - `-h, --help`
   - `--version`
   - `-q, --quiet` / `-v, --verbose` (define exactly)
   - `--json` / `--plain` (if applicable)
6. **I/O contract**:
   - stdout:
   - stderr:
7. **Exit codes**:
   - `0` success
   - `1` generic failure
   - `2` invalid usage (parse/validation)
8. **Env/config**:
   - env vars:
   - config file path + precedence:
9. **Examples**:
   - …

## Notes

- Prefer recommending a parsing library (language-specific) only when asked; otherwise keep this skill language-agnostic.
- If the request is "design parameters", do not drift into implementation.
