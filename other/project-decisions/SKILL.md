---
name: project-decisions
description: >
  Manage PROJECT_DECISIONS.md — a structured log of decisions made during
  meetings, extracted from 02.Meetings/summaries/ using the Anthropic API.
  File is organised by date (newest first), with categories as sub-sections
  under each date: architectural, technical, team management, project management,
  process, security & compliance, and cost & governance.
  Supports backfill (process all existing summaries), processing individual
  files, manual add, show by date/category, and keyword search.
  Use when asked to "extract decisions from meetings", "update project decisions",
  "what was decided about X", "add a decision", "show decisions", "backfill
  decisions", or invokes /project-decisions.
---

# Project Decisions Skill

Reads meeting summaries from `02.Meetings/summaries/`, sends them to Claude
for decision extraction, and maintains a structured Markdown file at
`00.Tasks/PROJECT_DECISIONS.md`.

Helper script: `extract_decisions.py` (relative to this skill file).

---

## Decision File Location

```
/home/gbencke/git.work/331.obsidian-scripts/00.Tasks/PROJECT_DECISIONS.md
```

---

## File Structure

Decisions are grouped by **date** (`## YYYY-MM-DD`), newest first. Under each
date, categories appear as `### Category` sub-sections. Only categories that
have decisions on that date are shown.

```
## 2026-05-29

### 🏗️ Architectural
- **Decision** — rationale *(Meeting Name)*

### 🔧 Technical
- **Decision** — rationale *(Meeting Name)*

---

## 2026-05-28
...
```

## Categories

| Key                    | Heading                  | Captures                                                                     |
| ---------------------- | ------------------------ | ---------------------------------------------------------------------------- |
| `architectural`        | 🏗️ Architectural        | System design, data models, integration patterns, infrastructure strategy    |
| `technical`            | 🔧 Technical             | Implementation choices, tools, parameters, performance targets               |
| `team_management`      | 👥 Team Management       | Ownership assignments, working-group formation, on-call processes            |
| `project_management`   | 📋 Project Management    | Scope, timelines, prioritization, deferrals, intake decisions                |
| `process`              | ⚙️ Process               | Cross-team agreements, meeting formats, coordination protocols               |
| `security_compliance`  | 🔒 Security & Compliance | Security remediations, access controls, audit requirements                   |
| `cost_governance`      | 💰 Cost & Governance     | Cost targets, vendor decisions, AI governance                                |
---

## Operations

### 1 — Backfill all summaries (full history)

```bash
nohup python3 /home/gbencke/.pi/agent/skills/project-decisions/extract_decisions.py \
  backfill \
  > /tmp/decisions_backfill.log 2>&1 &
echo "PID: $!"
```

Optional flags:
- `--since YYYY-MM-DD` — only process summaries on or after this date
- `--limit N` — cap at N files (useful for testing)
- `--dry-run` — print decisions without writing anything

Check progress:
```bash
tail -f /tmp/decisions_backfill.log
```

The script tracks processed files in `.decision_state.json` (relative to the
skill file). Re-running is safe — already-processed files are skipped.

### 2 — Process specific summary file(s)

```bash
python3 /home/gbencke/.pi/agent/skills/project-decisions/extract_decisions.py \
  process \
  "/home/gbencke/git.work/331.obsidian-scripts/02.Meetings/summaries/2026.05.29.PlatformSync.Summary.md"
```

Multiple files can be listed in one command. Use this after adding a new
meeting summary to keep the decisions file current.

### 3 — Manually add a decision

```bash
python3 /home/gbencke/.pi/agent/skills/project-decisions/extract_decisions.py \
  add "Decision statement" \
  --category architectural \
  --rationale "One-sentence context or reason" \
  --meeting "Meeting Name" \
  --date "2026-05-31"
```

- `--date` defaults to today if omitted.
- `--rationale` and `--meeting` are optional but strongly recommended.

Valid `--category` values: `architectural`, `technical`, `team_management`,
`project_management`, `process`, `security_compliance`, `cost_governance`.

### 4 — Show decisions

```bash
# All categories
python3 /home/gbencke/.pi/agent/skills/project-decisions/extract_decisions.py show

# Single category
python3 /home/gbencke/.pi/agent/skills/project-decisions/extract_decisions.py \
  show --category architectural
```

### 5 — Search decisions

```bash
python3 /home/gbencke/.pi/agent/skills/project-decisions/extract_decisions.py \
  search "Kinesis"
```

Case-insensitive. Prints every matching bullet prefixed with `[date] [category]`.

---

## Workflow Guidance

### After each new meeting summary is added

When new summaries land in `02.Meetings/summaries/`, process them immediately:

```bash
python3 /home/gbencke/.pi/agent/skills/project-decisions/extract_decisions.py \
  process \
  "/home/gbencke/git.work/331.obsidian-scripts/02.Meetings/summaries/FILENAME.md"
```

### Weekly review

To see all decisions from the past week, search by date or use `show` and
filter visually. For a focused view on a topic:

```bash
python3 /home/gbencke/.pi/agent/skills/project-decisions/extract_decisions.py \
  search "Aurora"
```

### Answering "what was decided about X?"

Use `search` first. If results are thin, open `PROJECT_DECISIONS.md` directly
in Obsidian — it is a standard markdown note with date sections at the top level.

---

## Bullet Format

Each decision is written as:

```
- **Decision statement** — rationale in one sentence *(Meeting Name)*
```

- The **statement** is a 3–12 word headline summarising the choice made.
- The **rationale** explains why, from the meeting context.
- The **source** in italics identifies the meeting.

---

## State File

```
/home/gbencke/.pi/agent/skills/project-decisions/.decision_state.json
```

Maps each processed summary file path to the timestamp it was processed.
Delete this file to force a full re-extraction from scratch.

---

## Environment

Requires `ANTHROPIC_API_KEY` to be set in the environment. Model: `claude-sonnet-4-5`.
