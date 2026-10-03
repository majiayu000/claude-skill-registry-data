---
name: obsidian-vault
description: Search, create, and manage notes in an Obsidian vault with wikilinks and index notes. Use when the user wants to find, create, or organize notes in Obsidian.
---

# Obsidian Vault

A personal-workflow integration. It assumes your notes live in an Obsidian vault on disk and
operates on them with the standard Read/Glob/Grep tools plus shell.

## Vault location

Set `OBSIDIAN_VAULT` in `.env` (see `.env.example`), then source it in your shell
(`set -a; . ./.env; set +a`) so the commands below resolve `$OBSIDIAN_VAULT`:

```bash
# .env
OBSIDIAN_VAULT="$HOME/Documents/notes"   # adjust to your vault
```

Typical subfolders (rename to match yours):

- `Daily Logbook/`: daily notes (managed by `/daily-note`)
- `Templates/`: note templates (e.g., `Daily Log.md`)

## Naming conventions

- **Index notes**: aggregate related topics (e.g., `Skills Index.md`, `RAG Index.md`)
- **Title Case** for all note names
- Daily notes use `YYYY-MM-DD.md` and live under `Daily Logbook/`

## Linking

- Use Obsidian `[[wikilinks]]` syntax: `[[Note Title]]`
- Notes link to dependencies/related notes at the bottom
- Index notes are just lists of `[[wikilinks]]`

## Workflows

### Search for notes

```bash
# Search by filename
find "$OBSIDIAN_VAULT" -name "*.md" | grep -i "keyword"

# Search by content
grep -rl "keyword" "$OBSIDIAN_VAULT" --include="*.md"
```

Or use the Grep/Glob tools directly on `$OBSIDIAN_VAULT`.

### Create a new note

1. Use **Title Case** for the filename
2. Write content as a unit of learning
3. Add `[[wikilinks]]` to related notes at the bottom
4. Place it in the appropriate subfolder (or the vault root for general index/topic notes)

### Find related notes

Search for `[[Note Title]]` across the vault to find backlinks:

```bash
grep -rl "\\[\\[Note Title\\]\\]" "$OBSIDIAN_VAULT"
```

### Find index notes

```bash
find "$OBSIDIAN_VAULT" -name "*Index*"
```

## Related

- The `/daily-note` skill manages the `Daily Logbook/` subfolder; defer to it for daily notes.
