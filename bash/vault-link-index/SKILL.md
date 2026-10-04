---
name: vault-link-index
description: Maintain the vault's link graph — find broken links, orphan notes, hub notes, and backlink gaps, and repair them with link-doctor. Use when the user says "broken links", "orphan notes", "fix links", "what links here", or "link health check". NOT for building/curating Maps of Content (use vault-moc-manager) or content-level issues like stubs and duplicates (use vault-cleanup-studio).
---

# Vault Link Index & Link Doctor

This skill manages the backlink index and provides link health tools for the vault.

## Files

- **Script**: `80_Code/scripts/generate-link-index.py`
- **Index**: `99_Attachments/link-index.json`

## Commands

### Smart Index Update
Default behavior - only regenerates if stale (>24h old):
```bash
python "80_Code/scripts/generate-link-index.py"
```

### Check Freshness Only
```bash
python "80_Code/scripts/generate-link-index.py" --check
```

### Force Regenerate
```bash
python "80_Code/scripts/generate-link-index.py" --force
```

### Find Broken Links (Link Doctor)
Show broken wikilinks with fuzzy-match suggestions:
```bash
python "80_Code/scripts/generate-link-index.py" --broken
```
Output example:
```
📄 20_Areas/Career/@data analyst.md
   ❌ [[&DataScienceHub 101]] → 💡 [[DataScienceHub 101]] (97% match)
```

### Show Orphan Notes
List notes with no incoming links, grouped by folder:
```bash
python "80_Code/scripts/generate-link-index.py" --orphans
```

## Link Doctor Operations

"Link Doctor" is not a separate script — it is `generate-link-index.py --broken`
(the detector) plus the repair rules below (the judgment). The detector emits each
broken link with fuzzy-match suggestions; you decide which class it falls into.

### Repair classes — apply vs ask

**Deterministic — apply directly**, then report the batch. These have exactly one
correct answer and no information is lost:

| Pattern | Cause | Fix |
|---------|-------|-----|
| `[[&Note]]` → `[[Note]]` | Prefix typo | Strip the leading `&` |
| `[[note]]` → `[[Note]]` | Case mismatch | Match the existing file's stem case exactly |
| `[[Old Name]]` where a rename map exists | Renamed note | Rewrite to the new name |

**Ambiguous — always ask first.** More than one plausible target, or the fix
destroys information:

| Situation | Why you must ask |
|---|---|
| Fuzzy match below high confidence, or 2+ candidate targets | Picking wrong silently rewires the graph |
| `[[2022-01-01]]` missing daily note | Create the note, or remove the link? Only the user knows |
| Broken link inside a quoted block or an archived note | The link may be a deliberate historical record |
| The "target" is a note the user just deleted | Deleting the link may be right — or the deletion was the mistake |

### Applying a fix

1. Read the source file (never edit blind from the index).
2. Replace the broken link — `Edit` with the exact old string.
3. Re-run `--broken` to confirm the count dropped and nothing new broke.

```python
# Deterministic class: prefix typo
old = "[[&DataScienceHub 101]]"
new = "[[DataScienceHub 101]]"
```

Never batch-apply an ambiguous class. Never "fix" a link by deleting it unless the
user said so.

## Obsidian CLI (Fast Queries) — with Fallbacks

Try CLI first for instant results. If Obsidian is not running, fall back to Python/Grep.

```bash
OBS="bash 80_Code/scripts/obs.sh"

# Check if Obsidian is available
$OBS --status

# Backlinks — what links TO this note?
$OBS backlinks file="Note Name"
$OBS backlinks file="Note Name" total          # count only
# FALLBACK: Grep for '\[\[Note Name' across *.md files

# Outgoing links — what does this note link TO?
$OBS links file="Note Name"
# FALLBACK: Read the file, extract [[...]] wikilinks

# Orphan notes (no incoming links)
$OBS orphans total
# FALLBACK: python "80_Code/scripts/generate-link-index.py" --orphans

# Dead-end notes (no outgoing links)
$OBS deadends total
# FALLBACK: no equivalent (would need full scan)

# Unresolved (broken) links
$OBS unresolved total
$OBS unresolved verbose                         # with source files
# FALLBACK: python "80_Code/scripts/generate-link-index.py" --broken
```

**When to use CLI vs Python script:**
| Need | Tool | Fallback |
|------|------|----------|
| Quick backlink lookup for 1 note | CLI `backlinks` | Grep `\[\[Note Name` |
| Count orphans/broken links | CLI totals | Python `--orphans` / `--broken` |
| Before moving/renaming a note | CLI `backlinks file=X` | Grep for wikilink |
| Broken links with fuzzy-match suggestions | Python `--broken` | (no CLI equivalent) |
| Full JSON index for bulk analysis | Python script | (always use Python) |
| Hub notes (most-referenced) | Python `top_linked` | (always use Python) |

## Query Operations

### Query Backlinks
**Try CLI first** (instant, live index):
```bash
bash "80_Code/scripts/obs.sh" backlinks file="Career-Development-Plan"
```

**Fallback** (if Obsidian not running):
1. Read `99_Attachments/link-index.json` → look up `backlinks["Note Name"]`
2. Or Grep for `\[\[Career-Development-Plan` across vault `*.md` files

### Find Hub Notes
Read the Python index, report `top_linked` (notes with most backlinks).

### Check Note Before Moving
1. CLI `backlinks file=X total` for instant count
2. If non-zero, show full backlink list
3. Proceed only after user confirms

## When to Use

| Situation | Action |
|-----------|--------|
| User asks "fix broken links" | Python `--broken` (has fuzzy suggestions) |
| Before refactoring files | CLI `backlinks` for quick check |
| Looking for orphaned notes | CLI `orphans total`, then Python `--orphans` for grouped list |
| Understanding vault structure | Python index hub notes |
| Moving/renaming a note | CLI `backlinks file=X` (instant) |
| Weekly maintenance | CLI `unresolved total` + `orphans total` for quick health check |
| "What links to X?" | CLI `backlinks file=X` |

## Index Structure

```json
{
  "generated": "ISO timestamp",
  "stats": {
    "total_files": 2379,
    "total_links": 8808,
    "orphan_count": 935,
    "broken_count": 2514
  },
  "orphans": ["path/to/orphan.md", ...],
  "top_linked": [["NoteName", 182], ...],
  "backlinks": {"NoteName": ["linking/file.md", ...]},
  "broken_links": {"source.md": ["BrokenTarget", ...]},
  "file_paths": {"NoteName": "actual/path.md"}
}
```

## Proactive Usage

Claude Code should invoke this skill:
- Before any batch file operations
- When user asks "what links to X?"
- When user asks about vault health/orphans/broken links
- Before archiving projects (check nothing links to them)
- After major file moves (run `--broken` to check for issues)
