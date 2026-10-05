---
name: hylo-memory
description: "Extract and update personal memories from Hylo notes into structured memory files. Use when the user wants to update their personal memory, extract memories from notes, run memory extraction, or refresh the personal memory base. Triggers on phrases like 'update my memory', 'extract memories from notes', 'run memory extraction', 'refresh personal memory', or any request to build or maintain a personal memory base from notes."
---

# Hylo Memory Extract

Extracts personal memories from short notes (`/_shorts`) and the knowledge base (`/_knowledge`) into six structured memory files under `/_memory/`. On first run (no memory files exist yet), scans the last 90 days for a rich initial snapshot. On subsequent runs, scans only the last 2 days. Memories not reinforced over time gradually fade and are eventually removed.

**Run all steps to completion without stopping or asking for confirmation.** Only speak at the final summary step.

---

## Inputs

1. **Self-introduction** — a brief description the user provides about themselves (name, role, projects, relationships, etc.). Used throughout extraction to identify personal content and disambiguate knowledge units. Ask for this if not provided.
2. **Extra scan paths** — additional vault path prefixes to scan beyond the two defaults (optional).
3. **Memory directory** — where memory files live (default: `/_memory/`).

---

## Step 1 — Determine run mode

Check whether any memory file already exists:

```bash
hylo read /_memory/_identity.md
```

- **First run** (file not found): set `scan_window = 90` days.
- **Incremental run** (file exists): set `scan_window = 2` days.

Record today's date as `today`.

Parse the self-introduction into an **author profile** to use as a lens throughout extraction:
- Name and known aliases/IDs
- Projects or products the author owns or runs (these may appear as vault directories or knowledge unit titles)
- Roles (creator, host, founder, etc.)
- People the author mentions as part of their personal life

This profile is critical for the knowledge base step: if a `source_notes` path falls under a directory that belongs to the author's own project (e.g. their own podcast, their own product), treat it as a **personal source**, not an external one.

---

## Step 2 — Collect content to process

Run both queries in parallel:

```bash
hylo short list --latest <scan_window> --limit 100
hylo knowledge list --kind knowledge --latest <scan_window> --limit 50
```

Also run `hylo list <path> --latest <scan_window>` for each extra scan path provided.

If all queries return zero results, skip to Step 4.

---

## Step 3 — Extract evidence

Apply different extraction rules depending on the source.

### Source A: Short notes (`/_shorts`)

`hylo short list` returns each entry's `content` inline — process directly, no file reads needed.

Short notes are the author's own unfiltered voice. Extract from **all six dimensions**:

| Dimension       | File              | What qualifies                                                                  |
| --------------- | ----------------- | ------------------------------------------------------------------------------- |
| **identity**    | `_identity.md`    | Stable facts: name, job title, location, family, languages                      |
| **preferences** | `_preferences.md` | Likes/dislikes, tools of choice, aesthetic tastes expressed as the author's own |
| **goals**       | `_goals.md`       | Active projects, ambitions, things the author is working toward                 |
| **beliefs**     | `_beliefs.md`     | Worldview, recurring opinions, values the author endorses                       |
| **people**      | `_people.md`      | Named individuals and their relationship to the author                          |
| **state**       | `_state.md`       | Near-term mood, current struggles, what is top of mind                          |

### Source B: Knowledge base (`/_knowledge`)

`hylo knowledge list` returns file paths. Read each unit:

```bash
hylo knowledge read <path>
```

**Classify each unit by its `source_notes` paths, using the author profile from Step 1:**

**Class 1 — Author's own content** (source_notes point to the author's own projects — e.g. their own podcast directory, their own product notes — or to personal paths like `/_shorts/`, `/journal/`)

The unit captures the author's own words or experience. Extract from **all six dimensions**, same as Source A.

**Class 2 — External source** (source_notes point to content produced by others — podcasts the author listened to, articles, clips)

Body content synthesises what the author heard or read, not their own views. Extract only:
- `## 立场` section → `beliefs` (the author's own dated opinion; skip if section absent)
- **Do not** extract people (third-party guests and case-study figures are not personal relationships)
- **Do not** extract from body sections like `## 核心启示`, `## 关键认知`, `## 核心定义` — these synthesise others' views

**Preferences from external sources — synthesize after all Class 2 units are read:**

Do not write per-unit `关注 X` entries. Instead:
1. Collect all Class 2 unit titles and tags into a pool.
2. Group into theme clusters by overlapping tags or subject matter.
3. For each cluster of ≥2 units, write **one synthesized preference item** describing the author's underlying orientation or taste — not a list of topics. The item should read like a trait, not a reading log. Example: units tagged `[indie-dev, startup]`, `[ai, startup]`, `[ai, llm]` → `对 AI 驱动的独立技术创业有持续投入，偏工程实践侧`.
4. Discard single-unit clusters — one reading is not a preference.

**Class 3 — No source_notes**

Treat as personal. Extract from all six dimensions.

**When classification is ambiguous**, use the author profile: if the directory or context matches something the author owns or created, prefer Class 1.

### Source C: Extra scan paths

Treat as personal notes. Extract from all six dimensions.

---

## Step 4 — Update memory files

For each dimension with new evidence, read the current file (if it exists), apply the update rules, then write the result.

### File format

```markdown
---
decay_window: <Xd>
last_updated: <YYYY-MM-DD>
---

## Active
- <item text> `last:<YYYY-MM-DD> seen:<N>`

## Fading
- <item text> `last:<YYYY-MM-DD> seen:<N>`
```

### Decay windows

| File              | decay_window |
| ----------------- | ------------ |
| `_identity.md`    | 365d         |
| `_beliefs.md`     | 90d          |
| `_preferences.md` | 90d          |
| `_people.md`      | 90d          |
| `_goals.md`       | 30d          |
| `_state.md`       | 7d           |

### Update rules (apply in this order)

**A — New evidence matches an existing Active item:** Update `last` to today, increment `seen`.

**B — New evidence matches a Fading item:** Promote to Active, update `last` to today, increment `seen`.

**C — New item not yet in the file:** Add to `## Active` with `last:<today> seen:1`.

**D — Active item with no new evidence:** If `(today − last) > decay_window`, move to `## Fading`. Do not change `last` or `seen`.

**E — Fading item with no new evidence:** If `(today − last) > 2 × decay_window`, delete entirely.

**F — Same fact, different wording:** Merge into one item — keep the clearer wording, sum `seen`, use the more recent `last`.

### Writing the file

```bash
hylo create /_memory/_<dimension>.md --content "<content>"           # new
hylo create /_memory/_<dimension>.md --content "<content>" --force   # overwrite
```

Only write files that actually changed.

---

## Step 5 — Summary

Report:
- Run mode (first run / incremental) and scan window used
- Items processed per source (shorts / knowledge / extra)
- Which memory files were updated
- Counts: added / refreshed / faded / deleted
- Deleted items by name (for user verification)
