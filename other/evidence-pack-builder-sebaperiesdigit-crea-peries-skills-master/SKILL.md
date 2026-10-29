---
name: evidence-pack-builder
description: Use when someone asks to build an evidence pack for this, document proof of this work, compile the evidence for this task, or needs a paper trail for completed work.
argument-hint: [task or topic]
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Write, Bash(cp *)
---

## What This Skill Does

Builds a reusable, traceable evidence pack for completed work — collecting the task brief, source references, dependencies, queries/scripts, raw extracts, validation results, screenshots, assumptions, limitations, edge cases handled, a decision log, and a final-output reference into one organized, auditable folder. Works the same way regardless of department or task type.

## Step 1: Identify the Task

- If `$ARGUMENTS` is provided, use it as the task name/topic.
- If empty, infer the task from what was just completed in the current conversation. If nothing recent is clearly a completed task, ask the user what task this evidence pack is for.
- Derive a filesystem-safe folder slug from the task name (lowercase, hyphens, no special characters).

## Step 2: Check for an Existing Pack

- Check whether `output/evidence-packs/<task-slug>/` already exists.
- If it does, ask via AskUserQuestion: overwrite in place, or save this run as `<task-slug>-v2/` (increment further if `-v2` also exists).
- If it doesn't, proceed to Step 3.

## Step 3: Auto-Extract What's Already Available

Scan the current conversation/session for each of the 12 components below. For each one found, capture it along with whatever metadata is available: **date**, **owner** (who performed/requested the work), **source system** (file path, database, API, tool), and **file references**.

1. **Task brief** — the original request/goal, as stated
2. **Source references** — files read, documents cited, systems queried
3. **Dependencies** — other systems, people, approvals, or timing this task relied on but didn't itself produce or verify (distinct from Source references, which is what was actually read/cited)
4. **Queries or scripts** — any commands, SQL, code, or tool calls actually run
5. **Raw extracts** — the actual data/output pulled from sources, unmodified
6. **Validation results** — checks that were actually performed and their outcomes (never inferred)
7. **Screenshots** — see Step 4
8. **Assumptions** — anything taken as given without explicit confirmation
9. **Limitations** — known gaps, caveats, or things not covered
10. **Edge cases handled** — exceptions, alternate paths, or unusual inputs encountered or considered during the work, and how each was handled
11. **Decision log** — key choices made during the task and why
12. **Final-output reference** — a link/path to the actual deliverable produced

## Step 4: Handle Screenshots

- If the user has already provided screenshot file paths (in this conversation or on request), copy each file into `screenshots/` inside the pack. Never move or modify the original files — copy only.
- If none are available, ask once via `AskUserQuestion`: "Do you have any screenshots to include as evidence?" — options `No, none to add` / `Yes, I'll provide file path(s)`. Mark `No, none to add (Recommended)` unless screenshots were already discussed earlier in the conversation, in which case mark `Yes` instead. If yes, ask directly as free text for the file path(s). If still none, record "No screenshots provided" in that section and continue — don't block the rest of the pack on this.

## Step 5: Fill Genuine Gaps

For any of the 12 components not found in Step 3 and not resolved in Step 4, ask the user directly — but only for what's actually missing. Don't re-ask about anything already captured from the conversation.

## Step 6: Redact Before Writing

Before writing anything to disk, scan all captured content (raw extracts, scripts, screenshot filenames, queries) for:

- Credentials, API keys, tokens, connection strings
- Personal or sensitive information (data tied to identifiable individuals beyond what's operationally necessary — e.g. emails, phone numbers, government IDs)

Redact matches with `[REDACTED]` before including them in any file. If a screenshot image itself likely contains sensitive on-screen content, flag it to the user rather than silently including or excluding it.

## Step 7: Confirm Before Writing

Before creating anything, show the user:
- The destination folder path (`output/evidence-packs/<task-slug>/`, or the `-v2`-style path chosen in Step 2)
- The full list of files that will be created
- A one-line status per component (Available / Not provided / Not applicable)

Ask via AskUserQuestion: **Write the evidence pack — Recommended** / **Cancel**. Only proceed to Step 8 after explicit confirmation. (This is separate from Step 2's overwrite-vs-versioned question, which only applies when a pack already exists — this gate applies every time, including a fresh pack.)

## Step 8: Write the Pack

Create `output/evidence-packs/<task-slug>/` (or `-v2` etc.) with:

- `README.md` — the evidence index (see Output Format below)
- `task-brief.md`
- `sources.md`
- `dependencies.md`
- `queries.md`
- `raw-extracts/` — one file per raw extract, unmodified
- `validation-results.md`
- `screenshots/` — copied images, or empty with a note if none
- `assumptions-and-limitations.md`
- `edge-cases.md`
- `decision-log.md` — each entry links to the specific raw-evidence file(s) that support it (e.g. "See `raw-extracts/query-1-output.csv`")
- `final-output.md` — reference/link to the actual deliverable

Keep raw evidence (`raw-extracts/`, `screenshots/`, `sources.md`, `queries.md`) strictly separate from analysis (`dependencies.md`, `decision-log.md`, `assumptions-and-limitations.md`, `edge-cases.md`, `final-output.md`). Analysis files must cite the raw file(s) behind each conclusion — never state a conclusion without pointing to its evidence.

Mark any of the 12 components not available as **Not provided** (info that should exist but wasn't given) or **Not applicable** (doesn't apply to this task) — never fabricate content to fill a gap.

## Step 9: Report

Tell the user what was written and where (the full folder path), and summarize which components are Available vs. Not provided/Not applicable.

## Output Format

`README.md` template — the evidence index:

```markdown
# Evidence Pack: {{ task name }}
**Date:** {{ date }}
**Owner:** {{ owner, if known }}
**Source system(s):** {{ systems/files involved, if known }}

## Index

| Component | Status | File |
|---|---|---|
| Task Brief | Available / Not provided / Not applicable | [task-brief.md](task-brief.md) |
| Source References | ... | [sources.md](sources.md) |
| Dependencies | ... | [dependencies.md](dependencies.md) |
| Queries/Scripts | ... | [queries.md](queries.md) |
| Raw Extracts | ... | [raw-extracts/](raw-extracts/) |
| Validation Results | ... | [validation-results.md](validation-results.md) |
| Screenshots | ... | [screenshots/](screenshots/) |
| Assumptions & Limitations | ... | [assumptions-and-limitations.md](assumptions-and-limitations.md) |
| Edge Cases Handled | ... | [edge-cases.md](edge-cases.md) |
| Decision Log | ... | [decision-log.md](decision-log.md) |
| Final Output | ... | [final-output.md](final-output.md) |
```

Each component file opens with the same metadata block (date, owner, source system, file references) where available, followed by its content.

## Notes

- Never modifies, moves, or deletes the original source/task files it's documenting — only reads from and copies into the pack.
- Never claims a validation check happened if it didn't — `validation-results.md` reflects only checks actually run.
- Redact before write, not after — never write unredacted content and clean it up later.
- Reusable across any department or task type — nothing in this skill assumes a specific team, tool, or file format.
- Not a replacement for the actual deliverable — it documents and proves the work, it doesn't do the work itself.
- Clickable-question convention: the overwrite-vs-versioned choice (Step 2), the write/cancel gate (Step 7), and the screenshot yes/no (Step 4) use `AskUserQuestion`. Step 1's task-identification question and Step 5's gap-filling questions stay free text — they're requests for the actual content (a task name, a source reference, a decision rationale), not a choice among a finite set of good answers.
