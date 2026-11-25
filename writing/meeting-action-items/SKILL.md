---
name: meeting-action-items
description: >
  Generate a per-person action items report from meeting summaries in
  02.Meetings/summaries/. Groups every action item by owner across all
  summaries (or a date range) and writes the result as a markdown file at the
  repo root. Use when asked to "generate action items from meetings", "create
  action items report", "summarize action items by person", "who owes what from
  meetings", or invokes /meeting-action-items.
argument-hint: "[YYYY-MM-DD or date range]"
---

# Meeting Action Items Skill

Reads meeting summaries from
`/home/gbencke/git.work/331.obsidian-scripts/02.Meetings/summaries/`,
extracts every action item, groups them by owner, and writes a single markdown
file at the repo root.

If an argument is provided (a date or date range such as `2026-05-01` or
`2026-05-01 to 2026-05-31`), process only summaries within that window.
Otherwise process all summaries.

---

## Step A — Collect summaries

1. List all files in `02.Meetings/summaries/` matching `*.Summary.md`, sorted
   by filename (date order).
2. If a date filter was provided, include only files whose embedded date
   (`YYYY.MM.DD` prefix) falls within the range.
3. If no files match, stop and report it.

---

## Step B — Extract action items

For each summary file:

1. Read the file in full.
2. Locate the `## Action Items` section (every summary has one).
3. Extract each bullet in the format:
   ```
   - **<Owner>**: <action text> *(HH:MM)*
   ```
   Also capture the meeting name from the file's frontmatter (`description`
   field or the filename title) and the meeting date from the filename prefix.
4. Build a record: `{ owner, action, time, meeting, date }`.

---

## Step C — Write the report

Output file:

```
<repo-root>/Meeting.Action.Items.<YYYY-MM-DD>.md
```

Use today's date in the filename (or the end date of the range if one was given).

**File structure:**

```markdown
# Meeting Action Items — <date or range>

## <Owner Name>

- **<action text>** *(Meeting Name, YYYY-MM-DD, HH:MM)*
- ...

---

## <Next Owner>
...
```

Rules:
- Sort owners alphabetically.
- Within each owner, sort items by date then time (oldest first).
- If the owner field is ambiguous (e.g. "Team", "Everyone"), list under
  `## Unassigned`.
- Include only action items — skip discussion bullets, decisions, and notes.
- Do not truncate or paraphrase action text; copy verbatim from the summary.

---

## Step D — Confirm output

After writing the file, print:

- Output path
- Total action items found
- Number of owners
- Date range covered
- Any summaries that had no `## Action Items` section (flag as a warning)
