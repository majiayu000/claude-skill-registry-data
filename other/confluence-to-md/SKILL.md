---
name: confluence-to-md
created_by: Aman Parmar
last_modified: 19-04-2026
description: |
  Convert Confluence pages to clean GitHub-Flavored Markdown files. Use this skill whenever the user
  wants to pull a Confluence page into the local repo, convert Confluence content to markdown, download
  a spec from Confluence, or batch-convert multiple pages. Also triggers on Confluence URLs, page IDs,
  or phrases like "pull this page", "download this spec", "confluence to md". Use this even if the user
  just pastes a Confluence URL and says something vague like "get this" or "convert this".
---

# Confluence to Markdown

Pull Confluence pages into the local repo as clean markdown. The bundled script handles all the messy
Confluence storage format edge cases (user mentions, complex tables, images, status badges) so you
don't have to. Zero LLM tokens spent on the actual conversion.

## Quick start

```bash
# Single page
python3 .claude/skills/confluence-to-md/scripts/confluence-to-md.py <page_id> <output_path>

# Batch (write a Python loop - don't run CLI commands one by one)
python3 scripts/batch-convert.py
```

The script auto-loads credentials from `.env` at the project root.

## Workflow

### Step 1: Get the page ID

Extract from the Confluence URL - it's the number in the path:
```
https://[your-instance].atlassian.net/wiki/spaces/[SPACE]/pages/1234567890/Page+Title
                                                                ^^^^^^^^^^ this
```

If the user gives a title instead of URL, search via API:
```bash
curl -s -u "$CONFLUENCE_EMAIL:$CONFLUENCE_TOKEN" \
  "$CONFLUENCE_BASE_URL/wiki/rest/api/content?spaceKey=[SPACE]&title=$(python3 -c 'import urllib.parse; print(urllib.parse.quote("Page Title"))')"
```

### Step 2: Pick the output path

Follow your project's naming conventions. A common pattern:

| Content type | Path pattern |
|---|---|
| Feature specs | `outputs/features/NNN-feature-name/feature-name.md` |
| Knowledge docs | `inputs/knowledge/slugified-title.md` |
| Cross-functional | `outputs/cross-functional/doc-name.md` |

**Folder naming** - strip from Confluence titles:
1. Author bracket tags: `[Author Name] SPEC | Feature` -> `feature`
2. Doc type prefixes: `SPEC |`, `PRD |`, `DOC |` -> remove
3. Phase numbers when a product name exists: `Phase 2 | Product Overview` -> use product name
4. Use the feature/product concept name, not the page description

### Step 3: Run the script

```bash
python3 .claude/skills/confluence-to-md/scripts/confluence-to-md.py 1234567890 outputs/features/001-my-feature/my-feature.md
```

### Step 4: Post-conversion check

1. Scan for raw HTML `<a>` tags with `data-*` attributes (embedded media) - replace with markdown links
2. Verify image references work (script downloads to `images/` subfolder automatically)
3. Check for excessive blank lines or formatting artifacts

## Batch conversion

Write a Python driver script for multiple pages:
```python
import subprocess
pages = {
    "1234567890": "outputs/000-topic-a/topic-a.md",
    "9876543210": "outputs/001-topic-b/topic-b.md",
}
for page_id, output_path in pages.items():
    subprocess.run(["python3", ".claude/skills/confluence-to-md/scripts/confluence-to-md.py", page_id, output_path], check=True)
```

## Index files (zero LLM tokens)

For overview pages, don't convert - parse programmatically:
1. Fetch page HTML via REST API (`body.storage`)
2. Parse `<ac:link>` tags with regex
3. Resolve titles to URLs via API
4. Write structured markdown

## What the script handles

The script automatically resolves these Confluence storage format quirks:
- `<time datetime="..."/>` self-closing tags
- `<ri:user>` mentions (resolves display names via API, cached)
- Bare `<ac:link>` without URLs (resolves from `body.view`)
- Complex tables with `numberingColumn`, `colgroup`, highlights
- Lists inside table cells (flattened to inline)
- Status macros -> `[Yes]`/`[No]` text
- Single-cell layout tables (unwrapped)
- `<ac:image>` attachments (downloaded to `images/`, handles CDN 302 redirects)

**Snapshot auto-save** — after every successful pull, the script saves a copy
to `.local/confluence-snapshots/<page_id>.md` (auto-creates the folder). This
baseline is the "last known sync" — every new pull overwrites it.

## Preflight check before pushing back (sibling script)

Whenever you later push changes back to the same Confluence page, run the
preflight FIRST to detect whether anyone edited that page on Confluence since
your last pull. Without this check, you can silently overwrite other people's
edits — a real-world incident that motivated this safeguard.

The preflight script lives inside this skill's `scripts/` folder (and also
inside `md-to-confluence/scripts/` — both copies work identically):

```bash
python3 .claude/skills/confluence-to-md/scripts/confluence-preflight.py <page_id> <local.md>
# OR equivalently:
python3 .claude/skills/md-to-confluence/scripts/confluence-preflight.py <page_id> <local.md>
```

Exit codes:
- **0** — Safe to push
- **1** — CONFLICT: Confluence has edits your local .md is missing. STOP and merge
- **2** — Error (credentials, network, etc.)

Use `--show-diff` to see full diffs, `--force` only if you deliberately want
to overwrite.

If something looks wrong in the output, read `references/storage-format-gotchas.md` for the full
list of 12 known issues and their fixes.

## Script location (IMPORTANT)

Scripts live INSIDE the skill folder, NOT in a shared `.claude/scripts/` folder:
- **Project**: `.claude/skills/confluence-to-md/scripts/confluence-to-md.py`
- **Global**: `~/.claude/skills/confluence-to-md/scripts/confluence-to-md.py`

**NEVER use symlinks** — always copy actual Python files. Symlinks break when the target moves.

Keep both locations in sync when modifying the script.

## Post-conversion evals

After conversion, automatically verify:
1. **No raw `<ac:` tags** — grep output for `<ac:` to catch unconverted Confluence macros
2. **No broken image refs** — if `images/` folder exists, verify every `![](images/...)` ref has a matching file
3. **Source header present** — first non-blank line after `# Title` should be `> Source: [Confluence](...)`
4. **No excessive blank lines** — no more than 2 consecutive blank lines anywhere in the file

## Dependencies

- Python 3 (standard library only)
- Pandoc (`brew install pandoc`)
- `.env` with: `CONFLUENCE_EMAIL`, `CONFLUENCE_TOKEN`, `CONFLUENCE_BASE_URL`
