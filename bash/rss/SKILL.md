---
name: rss
description: An RSS client that executes commands using Markdown-defined state/action rules.
---

# RSS Skill

## Overview

Use this package to execute rss operations through markdown-defined parsing and state transitions.
The command language is CLI-like, but execution is happening exclusively through markdown-native primitives (store/network/output actions).

Preserve defined behavior in strict mode, including:

- command tree and aliases
- flag and positional parsing rules
- env/config/flag precedence
- side effects (filesystem/network/env)
- output contracts and exit codes

## Trigger

Run this skill when the user asks to read or manage RSS feeds and provide a command string, for example:

- `--json feed ls`
- `read --limit 20 --unread`
- `export json --output out.json`

The provided command string is parsed as CLI-like syntax. It is an input contract, not a shell command to execute directly. The runtime will interpret it according to the defined grammar and execute the corresponding actions. 

Alternatively the command can be provided as natural language text, for example: 

- "Show me my unread feeds."
- "Add this RSS feed: <url> with the name 'Tech News'."
- "Export all my feeds to a JSON file named 'feeds.json'."
in which case the runtime will attempt to parse it into a valid command.

The runtime must:

1. Parse using `RUNTIME/COMMAND_GRAMMAR.md`.
2. Execute transitions in `RUNTIME/STATE_MACHINE.md`.
3. Execute primitive actions from `RUNTIME/EXECUTION_PRIMITIVES.md`.
4. Maintain runtime data in `RUNTIME/RUNTIME_CONTEXT.md`.
5. Emit errors from `RUNTIME/ERRORS.md` and exit via `RUNTIME/EXIT_CODES.md`.

First-run behavior: missing config and missing store are valid. The runtime must continue with defaults, bootstrap the store path, and initialize empty store state.
When `is_first_run=true`, the runtime should offer optional onboarding. If the user accepts, guide these 3 starter commands in order:
1. `config show`
2. `feed add <url> [-n name]`
3. `read --unread --limit 20`

## Execution Workflow

1. Normalize aliases and parse argv.
2. Resolve effective configuration and environment values.
3. Dispatch to the canonical command family.
4. Execute primitive actions and record side effects.
5. Format output according to output-mode precedence.
6. Exit with mapped code.

## Hard Rules

1. Preserve command semantics from the baseline behavior (`strict` mode).
2. Do not silently skip failure branches.
3. Log every mutating side effect in `side_effect_log`.
4. Treat missing dependencies (network, local analysis capability, permissions) as guarded failure transitions.
5. Do not claim behavior not covered in the documented runtime contracts and examples.
6. Do not invoke another RSS command binary to execute RSS commands.
7. Do not use "wrap original binary" fallback for in-scope commands.
8. If a primitive dependency is unavailable, transition to explicit failure state (`manual handoff` only for out-of-scope conditions).

## References

- [COMMANDS.md](COMMANDS.md)
