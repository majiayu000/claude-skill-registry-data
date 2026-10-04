---
name: wiki-sync
description: Sync game design wiki with current codebase state. Finds stale data, missing pages, contradictions.
trigger: /wiki-sync
---

# /wiki-sync

Audit and sync the Hexbound game design wiki (`wiki/`) with the current state of code and docs.

## When invoked

Run ALL steps in order. Do not skip steps.

### Step 1 — Detect changes since last sync

Read `wiki/log.md` to find the date of the last sync entry. Then check what changed:

```bash
# Find files changed since last wiki update
LAST_DATE=$(grep "^## \[" wiki/log.md | tail -1 | sed 's/## \[\(.*\)\].*/\1/')
echo "Last wiki update: $LAST_DATE"

# Check game system files for changes
git log --since="$LAST_DATE" --max-count=200 --name-only --pretty=format: -- \
  backend/src/lib/game/ \
  docs/06_game_systems/ \
  docs/02_product_and_features/ECONOMY.md \
  docs/02_product_and_features/GAME_SYSTEMS.md \
  | head -n 2000 | sort -u | grep -v '^$'
```

If no files changed, report "Wiki is up to date" and stop.

### Step 2 — Read changed files

For each changed file, read it and extract:
- New or modified constants/formulas
- New game mechanics or rule changes
- Removed or deprecated features

### Step 3 — Compare with wiki

For each change found, read the corresponding wiki page and check:
- **Stale data:** wiki says X, code now says Y → update wiki
- **Missing coverage:** new mechanic not in wiki → create page
- **Contradictions:** wiki page A says X, wiki page B says Y → flag

### Step 4 — Update wiki pages

For each stale/missing item:
1. Update or create the wiki page
2. Add/update `[[wiki-links]]` cross-references
3. Update `sources:` frontmatter with new source files

### Step 5 — Lint check

Run a full wiki health check:

```bash
cd wiki && echo "=== Broken links ===" && \
grep -roh '\[\[[^]]*\]\]' . | sed 's/\[\[//;s/\]\]//;s/|.*//' | sort -u | \
while read link; do
  [ "$link" = "filename" ] || [ "$link" = "Related Page 1" ] || [ "$link" = "Related Page 2" ] || [ "$link" = "wiki-links" ] && continue
  found=$(find . -name "$link.md" 2>/dev/null | head -1)
  [ -z "$found" ] && echo "  BROKEN: [[$link]]"
done && \
echo "=== Orphan pages (no inbound links) ===" && \
for f in $(find . -name "*.md" -not -name "schema.md" -not -name "index.md" -not -name "log.md"); do
  name=$(basename "$f" .md)
  refs=$(grep -rl "\[\[$name\]\]\|\[\[$name|" . --include="*.md" | grep -v "$f" | wc -l)
  [ "$refs" -eq 0 ] && echo "  ORPHAN: $name"
done && \
echo "=== Stats ===" && \
echo "  Pages: $(find . -name '*.md' -not -name 'schema.md' -not -name 'index.md' -not -name 'log.md' | wc -l)" && \
echo "  Wiki-links: $(grep -roh '\[\[[^]]*\]\]' . | wc -l)"
```

### Step 6 — Update index and log

1. Update `wiki/index.md` with any new pages
2. Append sync entry to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] sync | Wiki sync

- **Files checked:** N changed since last sync
- **Pages updated:** list
- **Pages created:** list
- **Contradictions found:** list or "none"
- **Broken links fixed:** N
- **Orphan pages:** list or "none"
```

### Step 7 — Report

Print a concise summary:
```
Wiki sync complete.
  Updated: N pages
  Created: N pages
  Contradictions: N
  Broken links: N
  Orphans: N
```
