---
name: career-development
description: "Analyzes skill gaps against your tracked jobs or a single posting, then builds a prioritized learning plan with real, web-searched resources. Activates on: upskill, skill gap, what should I learn, /upskill."
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebSearch
  - WebFetch
---

## Purpose

This file is the Plane 1 knowledge anchor for the Career Development workflow
(ARCH-0040). As a Plane 1 skill it lives under `.claude/skills/career-development/`
and provides structured knowledge — it does not execute binaries. When activated, it
compares the candidate's current skills against demand (either every job in the tracker,
or one target posting), produces a prioritized gap heatmap, finds real learning
resources via web search, sequences them into a study order, and persists a markdown
report under `upskill/`. It operates under the no-fabrication rule (ARCH-0007), the
read-before-write invariant, and never invents learning resources.

This skill backs the `/upskill` command (`.claude/commands/upskill.md`) and the
dashboard's Upskill surface, which reads the reports this skill writes
(`upskill/report-*.md`).

## Trigger Phrases

- "/upskill" (with or without a job URL)
- "What should I learn for <role/company>?"
- "Where are my skill gaps?"
- "Analyze my upskilling needs"
- Any phrase about skill gaps, learning plans, or closing the distance to a target role

## Companion Files

| File | When to Read |
|------|--------------|
| `../job-application-assistant/01-candidate-profile.md` | Always — the source of the candidate's *current* skills, education, and experience to diff against |
| `../job-application-assistant/04-job-evaluation.md` | For the candidate's stated strong/weak areas and career goals, to weight and frame gaps |

This skill also reads, outside the skill directory:

| Source | Mode | Purpose |
|--------|------|---------|
| `job_search_tracker.csv` (repo root) | Aggregate | Role, company, and `fit_rating` per tracked application |
| `upskill/report-YYYY-MM-DD.md` (most recent) | Aggregate | Previous report, for delta comparison (REQ-3010) |
| Job posting (URL or pasted text) | Targeted | The single posting to analyze |

---

## Workflow

The skill runs the same six analytical stages in both modes; what differs is the input
and how priority is computed.

### Stage 0 — Mode selection & data loading (REQ-3001, REQ-3002, REQ-3003)

Decide the mode from the invocation:

- **Aggregate** — no argument. Analyzes all tracked jobs.
  - Read `job_search_tracker.csv`; for each row extract role, company, and `fit_rating`.
  - If the tracker is missing or has only its header row, do **not** write an empty
    report — tell the user honestly: *"You have no tracked applications yet. Run `/search`
    and `/apply` first, or give me a job URL for a targeted analysis (`/upskill <url>`)."*
  - Read the candidate profile (`01-candidate-profile.md`) for current skills.
  - Glob `upskill/report-YYYY-MM-DD.md` and load the most recent for delta (REQ-3010).
- **Targeted** — `/upskill <url>` or pasted posting text. Analyzes one posting.
  - Fetch the posting with `WebFetch`. If the fetch fails, ask the user to paste the
    posting text (DEC-011) — never abort.
  - Extract: title, company, required skills, preferred skills, responsibilities, domain
    context.
  - Read the candidate profile. **Do not** read the tracker in targeted mode.

The report's date is today's date (`YYYY-MM-DD`), available from context.

### Stage 1 — Pass 1: hard-skill diff (REQ-3004)

Extract required and preferred **technical** skills from the source(s) and diff against
the profile.

- **Aggregate:** build a skill-frequency map weighted by fit —
  `gap_weight(skill) = sum over postings mentioning it of ((100 − fit_rating) / 100 × occurrence)`.
  Lower-fit jobs contribute more (the candidate is further from those roles).
- **Targeted:** list required skills before preferred, equal weight, alphabetical within
  each group.
- Remove any skill already present in the profile in **any form** — match generously:
  "Python" covers "Python scripting"; "AWS" covers "Amazon Web Services".

### Stage 2 — Pass 2: LLM synthesis (REQ-3005)

Reason holistically about gaps mechanical diffing misses. Consider and tag each:

- `[domain]` — domain/industry knowledge gaps
- `[soft]` — soft-skill gaps (leadership, stakeholder management, communication)
- `[tooling]` — tooling/process gaps (CI/CD, IaC, agile practices)
- `[credential]` — certifications/credentials. Flag a credential gap only when **multiple
  postings** list it as preferred (aggregate) or it is explicitly required (targeted).

No duplication with Pass 1.

### Stage 3 — Gap heatmap (REQ-3006, REQ-3011)

Combine Pass 1 + Pass 2 into a prioritized table, printed to the terminal **before** the
learning plan:

| Priority | Skill / Area | Type | Gap Source |
|----------|-------------|------|------------|

- Priority levels: **Critical · High · Medium · Low**.
- Aggregate: priority follows the fit-weighted frequency score (higher score → higher
  priority).
- Targeted: required → Critical/High, preferred → Medium, inferred (Pass 2) → Medium/Low.
- **Low** gaps appear in the heatmap for completeness but receive **no** learning-plan
  entry unless the user asks (REQ-3011).

### Stage 4 — Learning plan (REQ-3007)

For every **Critical** and **High** gap (and **Medium** gaps too if the total gap count
is fewer than 5), produce a learning entry:

- 2–3 resources, each with **name, URL, and a one-line reason**.
- **Resources must come from a real `WebSearch`** — never fabricated (ARCH-0007). Include
  the current year in queries so results are fresh.
- Resource preference order: hands-on courses > lecture-only; official docs for tooling;
  books for domain knowledge.
- A **study direction** tailored to the candidate's background: what they can skip given
  what they already know, and where to start.
- A **time estimate**.
- Group entries by theme (e.g. *Cloud & Infrastructure*, *MLOps*, *Domain Knowledge*).

If a genuine resource cannot be found for a gap, say so plainly rather than inventing one.

### Stage 5 — Study order (REQ-3008)

Suggest a numbered, dependency-aware sequence:

| # | Topic | Type | Estimated Time | Note (dependencies) |
|---|-------|------|----------------|---------------------|

Ordering rules: dependencies first → Critical before High before Medium → quick wins
early → domain knowledge last. Show the **total estimated time** at the bottom.

### Stage 6 — Persist the report (REQ-3009) & delta (REQ-3010)

**Always** write the report, even if the user seems satisfied with the terminal output.

- Aggregate → `upskill/report-YYYY-MM-DD.md`
- Targeted → `upskill/report-YYYY-MM-DD-<company-slug>-<role-slug>.md`

Slugs are lowercase, hyphen-separated, alphanumeric. The report contains, in order:

1. **Delta** (aggregate only, when a previous report exists): *Gaps closed* — skills from
   the previous heatmap now present in the profile; *New gaps* — skills in the current
   heatmap not in the previous report. Omit this section in targeted mode or when no
   previous report exists.
2. Gap heatmap (Stage 3)
3. Learning plan (Stage 4)
4. Study order (Stage 5)

Reports are personal output: written under `upskill/`, never modified after creation, and
git-ignored. The dashboard's Upskill surface renders them as-is.

---

## Contract

- **No fabrication (ARCH-0007):** every learning resource is real and web-searched; every
  URL resolves. An empty tracker or unfetchable posting yields an honest message, not a
  fabricated or empty report.
- **Read-before-write:** read the profile (and previous report in aggregate mode) before
  writing anything.
- **Generous skill matching:** a gap is only a gap if the profile lacks it in every form.
- **Modes never cross streams:** targeted mode ignores the tracker; aggregate mode does
  not fetch a posting.
- **Career framing:** use `04-job-evaluation.md`'s stated goals and strong/weak areas to
  frame priorities — a gap that blocks the candidate's stated direction outranks an
  incidental one.
