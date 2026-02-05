---
name: commands-frontmatter-adapter
description: Parse Claude command frontmatter and expose body/meta for Codex CLI.
---

# Commands Frontmatter Adapter

Extract frontmatter and body from Claude-style command files so Codex CLI can consume the body as a prompt while still exposing metadata as JSON.

## Usage

- By command name (from the scripts directory): `./adapter.py --command diary --pretty`
- By explicit file (from anywhere): `/abs/path/to/adapter.py --file /abs/path/to/src/.claude/commands/diary.md`

Note: The script resolves `src/.claude/commands` relative to the skill location, so symlinked global installs work without depending on the current working directory. Use `--file` if your commands live elsewhere.

## Options

- `--body-only` Output body only (paste into prompt)
- `--frontmatter-only` Output parsed frontmatter as JSON
- `--raw-frontmatter` Output raw frontmatter block
- `--pretty` Pretty-print JSON

## Behavior

1. Treat the first `---` ... `---` block as frontmatter.
2. Try `yaml.safe_load`; if PyYAML is missing or fails, fall back to a minimal parser (key/value and bullet lists).
3. JSON output structure:
   - `file`: target file path
   - `frontmatter`: parsed metadata (dict or null)
   - `frontmatter_raw`: raw text
   - `body`: body text

## Known frontmatter keys (current commands)

- `description`: short summary shown in command picker.
- `argument-hint`: usage hint for `$ARGUMENTS`.
- `allowed-tools`: tool whitelist string (pass-through; no validation here).

The adapter performs parsing only; interpretation or enforcement of these keys is left to the caller (e.g., Codex CLI prompt wrappers).

## Tips

- Prefer `--body-only` when piping into Codex CLI prompts.
- Manually respect metadata such as `allowed-tools` as needed in your session.
- If a file has no frontmatter, only the body is returned.
