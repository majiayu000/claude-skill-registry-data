---
name: action-items
description: >
  Manage Guilherme Bencke's personal action-item log at
  00.Tasks/ACTION_ITEMS.guilherme_bencke.md. Supports adding new items under
  today's date (or any explicit date), showing recent items, and searching by
  keyword across the full history.
  Use when asked to "add action item", "log an action item", "update my action
  items", "add to my TODO", "show my recent action items", "search action
  items", or invokes /action-items.
---

# Action Items Skill

Reads and writes
`/home/gbencke/git.work/331.obsidian-scripts/00.Tasks/ACTION_ITEMS.guilherme_bencke.md`.

The file is organised as date sections (`## YYYY-MM-DD`, newest first). Each
section holds a table whose rows are sorted by sub-topic:

```
| ★ | Sub-topic | Action |
|---|---|---|
|   | [[_Scheduling.Rules]] | **Guilherme Bencke**: <action text> *(<Meeting name>, <timestamp>)* |
```

The sub-topic is a `_*.md` note listed in `00.Tasks/Topics/All Sub-Topics.md`.
Rows with no matching sub-topic use `—` and sort last. Sections before
2026-09 keep the old two-column `| ★ | Action |` table; `add` writes the old
format into those sections.

All operations go through the helper script at `action_items.py` (relative to
this skill file).

**Auto-linking:** when `add` writes a row, it looks for a file in
`02.Meetings/summaries/` whose date and name match `--date` + `--meeting`
(case/space-insensitive) and turns the meeting name into a wikilink to that
note, e.g. `*([[2026.08.14.DailySync.Summary|Daily Sync]], 12:00)*`. If no
matching file is found, the meeting name is left as plain text. Combined
names like `Daily Sync / Platform Sync Mapping` are resolved part by part.

---

## Operations

### 1 — Add an action item

```bash
python3 /home/gbencke/.pi/agent/skills/action-items/action_items.py add \
  "ACTION TEXT" \
  [--meeting "Meeting Name"] \
  [--time "HH:MM"] \
  [--date "YYYY-MM-DD"] \
  --subtopic "_Sub.Topic"
```

- `action text` — the full action description (required)
- `--meeting` — meeting or source name (default: `Manual Entry`)
- `--time` — timestamp inside the meeting, e.g. `14:32` (optional)
- `--date` — target date in `YYYY-MM-DD` format (default: today)
- `--subtopic` — **required**. Sub-topic note name from `All Sub-Topics.md`,
  e.g. `_Scheduling.Rules`. Pick the best match; pass `—` only when none fits
  (team management, hiring, one-off production tickets). The script rejects
  names that are not in the index.

**Behaviour:**
- If the target date section already exists, the row is added to its table
  and the table is re-sorted by sub-topic (stable).
- If the date section does not exist, a new `## YYYY-MM-DD` section is created
  at the top of the date list (above all existing date sections).

### 2 — Show recent items

```bash
python3 /home/gbencke/.pi/agent/skills/action-items/action_items.py show \
  [--days N]
```

- `--days` — how many past days to include (default: 7)

Prints all sections whose date is within the window, preserving the original
formatting.

### 3 — Search by keyword

```bash
python3 /home/gbencke/.pi/agent/skills/action-items/action_items.py search \
  "KEYWORD"
```

Case-insensitive full-text search across all bullet lines. Prints each match
prefixed with its date section.

---

## Workflow Guidance

### Adding items from a meeting summary

When the user provides a list of action items from a meeting (e.g. extracted
from a transcript or summary), add each one individually with the same
`--meeting` and `--date` values:

```bash
python3 /home/gbencke/.pi/agent/skills/action-items/action_items.py add \
  "Follow up with Rebecca on the API contract" \
  --meeting "PlatformSync" --time "14:15" --date "2026-05-31"

python3 /home/gbencke/.pi/agent/skills/action-items/action_items.py add \
  "Review Hasitha's PR before Thursday" \
  --meeting "PlatformSync" --time "22:30" --date "2026-05-31"
```

### Adding a manual (no-meeting) item

```bash
python3 /home/gbencke/.pi/agent/skills/action-items/action_items.py add \
  "Draft the Aurora consolidation proposal" \
  --meeting "Daily Note"
```

### Showing today's items

```bash
python3 /home/gbencke/.pi/agent/skills/action-items/action_items.py show --days 1
```

---

## File Location

```
/home/gbencke/git.work/331.obsidian-scripts/00.Tasks/ACTION_ITEMS.guilherme_bencke.md
```

The file is an Obsidian markdown note. Do not reformat other content — the
script only adds a row and re-sorts the rows of the target date's table.

---

## Output Format After Adding

After each `add` call, confirm to the user with a brief summary:

> Added to **2026-05-31**:
> - **Guilherme Bencke**: Follow up with Rebecca on the API contract *(PlatformSync, 14:15)*

If multiple items were added in one request, list them all together grouped by
date.
