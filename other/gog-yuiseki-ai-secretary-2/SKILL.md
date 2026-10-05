---
name: gog
description: Operate the gog CLI for Gmail, Calendar, Drive, and related Google services. Use when a user asks to run or debug gog commands, inspect flags, automate gog workflows, or validate auth/output behavior with real command execution.
---

# Gog Skill

Use this skill to execute `gog` commands safely and reliably in this repo.

## Preflight

1. Verify binary and command tree.
```bash
./bin/gog --help
./bin/gog schema --help
```
2. Verify config and keyring backend.
```bash
./bin/gog config path
./bin/gog auth status
./bin/gog auth keyring
```
3. Set account explicitly for API commands.
```bash
./bin/gog --account <email> gmail --help
```

## Auth and TTY Rules

- Prefer `--account <email>` on every API command.
- In this environment (`keyring_backend=file`), token reads can fail in non-TTY sessions with:
  `no TTY available for keyring file backend password prompt`.
- When that happens, run the command in a TTY session and submit passphrase interactively.
- If running fully non-interactive, set a usable `GOG_KEYRING_PASSWORD` value for the configured keyring.

## Output Rules

- Use `--json` for automation and agents.
- Use `--plain` for stable TSV output.
- Use rich text only for human inspection.
- Add `--no-input` in CI/automation.

## Safe Execution Order

1. Inspect help/schema first.
2. Run read commands before write commands.
3. For write commands, run `--dry-run` first.
4. Use `--force` only when the user explicitly wants to skip confirmations.

## Verified Command Patterns

The following patterns were validated against `./bin/gog` in this repository.

### Discovery

```bash
./bin/gog gmail --help
./bin/gog calendar --help
./bin/gog drive --help
./bin/gog tasks --help
./bin/gog send --help
./bin/gog ls --help
./bin/gog open --help
```

### Read Operations

```bash
./bin/gog --account <email> gmail labels list --plain
./bin/gog --account <email> gmail search 'newer_than:1d' --max 1 --plain
./bin/gog --account <email> calendar events primary --today --max 1 --plain
./bin/gog --account <email> drive ls --max 1 --plain
./bin/gog time now --json
```

### Write Operation (Dry Run First)

```bash
./bin/gog --dry-run --account <email> send --to <email> --subject 'dry run test' --body 'hello' --plain
```

## Troubleshooting

- `missing --account`: add `--account <email>` or set `GOG_ACCOUNT`.
- `no TTY available for keyring file backend password prompt`: run in TTY or provide `GOG_KEYRING_PASSWORD`.
- `unknown flag`: check command-local help (`./bin/gog <group> <command> --help`).
- Empty results should be explicit in automation: add `--fail-empty` where supported (for example `gmail search`, `calendar events`).

## Agent Defaults

For scripted runs, prefer:

```bash
./bin/gog --account <email> --json --no-input <command...>
```

Then narrow payloads with command-level filters (for example `--max`, `--fields`, `--query`) and parse with `jq` only after validating output shape.
