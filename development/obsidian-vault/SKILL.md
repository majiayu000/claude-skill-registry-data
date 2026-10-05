---
name: obsidian-vault
category: obsidian
description: Search, create, and manage notes in the Obsidian vault with wikilinks and index notes. Use when user wants to find, create, or organize notes in Obsidian.
related-skills:
  - obsidian-markdown
  - obsidian-canvas
loop-eligible: false

compatibility: claude-code codex opencode
---

# Obsidian Vault

## Vault location

Assume the user is running this skill from inside a vault. Resolve the vault root using git:

```bash
VAULT=$(git rev-parse --show-toplevel)
```

All commands below use `$VAULT`. Mostly flat at root level.

## Naming conventions

- **Index notes**: aggregate related topics (e.g., `Ralph Wiggum Index.md`, `Skills Index.md`, `RAG Index.md`)
- **Title case** for all note names
- No folders for organization - use links and index notes instead

## Linking

- Use Obsidian `[[wikilinks]]` syntax: `[[Note Title]]`
- Notes link to dependencies/related notes at the bottom
- Index notes are just lists of `[[wikilinks]]`

## Workflows

### Search for notes

```bash
VAULT=$(git rev-parse --show-toplevel)

# Search by filename
find "$VAULT" -name "*.md" | grep -i "keyword"

# Search by content
grep -rl "keyword" "$VAULT" --include="*.md"
```

Or use Grep/Glob tools directly on the vault path.

### Create a new note

1. Use **Title Case** for filename
2. Write content as a unit of learning (per vault rules)
3. Add `[[wikilinks]]` to related notes at the bottom
4. If part of a numbered sequence, use the hierarchical numbering scheme

### Find related notes

Search for `[[Note Title]]` across the vault to find backlinks:

```bash
VAULT=$(git rev-parse --show-toplevel)
grep -rl "\\[\\[Note Title\\]\\]" "$VAULT"
```

### Find index notes

```bash
VAULT=$(git rev-parse --show-toplevel)
find "$VAULT" -name "*Index*"
```

### Find untagged references

Detect note titles mentioned in prose that aren't wrapped in `[[wikilinks]]`. This catches references the author forgot to link.

1. Build a list of all note titles (filenames without `.md`)
2. For each title, search the vault for occurrences that are NOT inside `[[ ]]`
3. Report the file, line, and unlinked mention

```bash
VAULT=$(git rev-parse --show-toplevel)

# Get all note titles
titles=$(find "$VAULT" -name "*.md" -printf '%f\n' | sed 's/\.md$//')

# For each title, find mentions not wrapped in [[ ]]
for title in $titles; do
  grep -rn --include="*.md" "$title" "$VAULT" \
    | grep -v "\[\[$title\]\]" \
    | grep -v "^.*/$title\.md:"
done
```

Or use Grep to search for a specific title and manually check which hits lack wikilink syntax.

### Find duplicate or misspelled tags

Detect tags that look like near-duplicates (case differences, typos, plural/singular variants).

1. **List all unique tags** across the vault:

```bash
VAULT=$(git rev-parse --show-toplevel)

grep -roh '#[A-Za-z0-9_/-]\+' "$VAULT" --include="*.md" \
  | sort | uniq -c | sort -rn
```

2. **Find case-insensitive duplicates** (e.g., `#RAG` vs `#rag` vs `#Rag`):

```bash
grep -roh '#[A-Za-z0-9_/-]\+' "$VAULT" --include="*.md" \
  | sort -u | awk '{lower=tolower($0); if (seen[lower]++) print prev[lower], $0; else prev[lower]=$0}'
```

3. **Spot low-frequency tags** that may be typos of common ones:

```bash
grep -roh '#[A-Za-z0-9_/-]\+' "$VAULT" --include="*.md" \
  | sort | uniq -c | sort -n | head -30
```

Review the low-count tags against the high-count list. Tags used only once or twice are likely misspellings of an existing tag.

4. **Find where a suspicious tag is used** so you can fix it:

```bash
grep -rn '#suspicioustag' "$VAULT" --include="*.md"
```

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/obsidian-vault.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
