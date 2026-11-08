---
name: create-cli
description: "CLI UX/spec: args, flags, help, output, errors, config, dry-run."
disable-model-invocation: true
---

# Create CLI

Design CLI surface area (syntax + behavior), human-first, script-friendly. For rich cli/tui apps read `skills/create-cli/references/opentui/SKILL.md` and related files.

## Do This First

- Read `agent-scripts/skills/create-cli/references/cli-guidelines.md` → apply as default rubric
- Upstream: https://clig.dev/ (propose changes: https://github.com/cli-guidelines/cli-guidelines)
- Ask only minimum clarifying questions to lock interface

## Clarify (fast)

Ask, then proceed with best-guess defaults if unsure:

- Command name + one-sentence purpose
- Primary user: humans, scripts, or both
- Input sources: args vs stdin; files vs URLs; secrets (never via flags)
- Output contract: human text, `--json`, `--plain`, exit codes
- Interactivity: prompts allowed? need `--no-input`? confirmations for destructive ops?
- Config model: flags/env/config-file; precedence; XDG vs repo-local
- Platform/runtime: macOS/Linux/Windows; single binary vs runtime

## Deliverables

Produce compact spec:

- Command tree + USAGE synopsis
- Args/flags table (types, defaults, required/optional, examples)
- Subcommand semantics (what each does; idempotence; state changes)
- Output rules: stdout vs stderr; TTY detection; `--json`/`--plain`; `--quiet`/`--verbose`
- Error + exit code map (top failure modes)
- Safety rules: `--dry-run`, confirmations, `--force`, `--no-input`
- Config/env rules + precedence (flags > env > project config > user config > system)
- Shell completion story (if relevant): install/discoverability; generation command or bundled scripts
- 5–10 example invocations (common flows; include piped/stdin)

## Default Conventions (unless user overrides)

- `-h/--help` always shows help, ignores other args
- `--version` prints version to stdout
- Primary data → stdout; diagnostics/errors → stderr
- `--json` for machine output; consider `--plain` for stable line-based text
- Prompts only when stdin is TTY; `--no-input` disables prompts
- Destructive ops: interactive confirmation + non-interactive requires `--force` or `--confirm=...`
- Respect `NO_COLOR`, `TERM=dumb`; provide `--no-color`
- Handle Ctrl-C: exit fast; bounded cleanup; crash-only when possible

## Template: CLI Spec Skeleton

Fill sections, drop irrelevant:

1. **Name**: `mycmd`
2. **One-liner**: `...`
3. **USAGE**: `mycmd [global flags] <subcommand> [args]`
4. **Subcommands**: `mycmd init ...` / `mycmd run ...`
5. **Global flags**: `-h, --help` / `--version` / `-q, --quiet` / `-v, --verbose` / `--json` / `--plain`
6. **I/O contract**: stdout: / stderr:
7. **Exit codes**: `0` success / `1` generic failure / `2` invalid usage
8. **Env/config**: env vars / config file path + precedence
9. **Examples**

## Notes

- Recommend parsing library only when asked; otherwise keep language-agnostic
- "Design parameters" request → don't drift into implementation
