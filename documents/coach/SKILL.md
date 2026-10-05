---
name: coach
description: Extract lessons from this session into Chatty's shared knowledge base — behavioral instincts (.claude/coach-lessons.md) and solution docs (docs/solutions/) — with minimal user effort. Run at the end of a working session, or whenever a gotcha worth keeping was discovered. Writes automatically; no approval step.
---

# coach

Reflect on the current session and auto-capture two types of knowledge:

1. **Instincts** — one-liner behavioral rules in `.claude/coach-lessons.md` that shape future sessions. Each carries an evidence record (confirmations, violations, last event date); proven instincts are promoted to CLAUDE.md.
2. **Solution docs** — detailed write-ups of non-trivial problems solved this session, in `docs/solutions/`.

The skill decides what's worth capturing and **writes everything automatically — no approval step, no review**. This is an AI-curated knowledge base: the skill self-curates (updates evidence, prunes, rewrites weak instincts) without asking. After writing, emit only a terse one-line summary; do NOT print a full debrief.

Optional arguments: `dry-run` (print proposed changes, write nothing), `instincts only`, `docs only`.

## Instinct Format

```
- `[✓2 ✗0 · 2026-07-11]` **When** <trigger> → **do** <action> → **because** <reason>
```

The bracket is the instinct's **evidence record**:

- `✓N` — confirmations: distinct sessions where the trigger arose and the instinct was followed (or self-corrected in time). Capture itself is NOT a confirmation — new instincts start `[✓0 ✗0 · <today>]`. At most +1 per instinct per session.
- `✗M` — violations: sessions where the trigger arose and a correction had to happen.
- Both fields are always present, even at zero (parseability beats prettiness).
- The date is the last evidence event of ANY kind (capture, confirm, or violate) — it drives dormancy detection.

A short prose clause ("reaffirmed on #NNN — <what happened>") may follow the because-clause when an episode carries unique detail not already on the line; the counts are authoritative for lifecycle decisions, the prose is color. A trailing `NOTE: …` marks a deliberate lifecycle decision (e.g. already covered by CLAUDE.md) — respect it instead of re-litigating.

## Steps

### 1. Gather state

Run in parallel:
- `git rev-parse --show-toplevel` (repo root), `git rev-parse --abbrev-ref HEAD`, `git log --oneline -10`
- Read `<repo-root>/.claude/coach-lessons.md`

Parse all existing instincts and their evidence records. Also determine the sweep cadence (used in step 8): read the `<!-- coach-last-sweep: <ISO timestamp> -->` comment near the top, then count commits since it: `git log --since='<timestamp>' --oneline -- .claude/coach-lessons.md | wc -l`. If the comment is missing, treat the sweep as due.

### 2. Analyze the session

Review the full conversation history. Classify the session:

| Session type | Instincts? | Solution doc? |
|-------------|------------|---------------|
| Substantial problem-solving (debugging, architecture, new feature with gotchas) | Yes | Yes |
| Routine work with corrections or discoveries | Yes | No |
| Quick questions, config changes, trivial fixes | Maybe | No |
| Trivial session (no real work) | Skip entirely | No |

If the session was trivial, say so and stop — don't force extraction.

### 3. Update evidence on existing instincts

For each existing instinct whose trigger condition arose during this session:
- **Followed** (adherence or self-correction): `✓+1`, refresh the date
- **Violated** (correction happened): `✗+1`, refresh the date
- **Not triggered**: leave the line untouched

Only evaluate instincts that were actually triggered. At most one evidence event per instinct per session.

### 4. Extract new instincts

Look for: corrections the user made, gotchas discovered during the work, patterns that worked well, mistakes caught and fixed, workflow improvements.

**Verified-only precondition:** an instinct derived from a bug fix or technical solution requires that the fix was actually verified this session (tests ran, live check, or user confirmation). If not verified, do NOT write a speculative lesson — note it in the summary as `skipped (unverified): <one-liner>`. Carve-out: user-correction and workflow-gotcha instincts are verified by the correction event itself.

**Filter aggressively — do NOT extract:**
- Generic advice ("write tests", "read the docs")
- One-off debugging details ("the typo was on line 42")
- Things already captured in existing instincts or in CLAUDE.md
- Speculative ideas that weren't validated
- Meta-process lessons ("use Claude for X")

### 5. Draft solution doc (if warranted)

Only when ALL are true: the session solved a non-trivial problem; the solution was **verified this session**; the problem required investigation (not just "change X to Y"); the solution has reuse value; no existing doc in `docs/solutions/` covers it (grep for module names / error messages first — if a high-overlap doc exists, update it instead).

Markdown file with YAML frontmatter in `docs/solutions/<category>/`:

```markdown
---
title: <descriptive title>
date: YYYY-MM-DD
category: <auto-detected>
module: <affected module>
tags: [<relevant tags>]
problem_type: <bug|performance_issue|pattern|convention|etc>
---

## Problem            (knowledge track: ## Context)
## Symptoms           (knowledge track: ## Guidance)
## What Didn't Work   (knowledge track: ## Why This Matters)
## Solution           (knowledge track: ## When to Apply)
## Why This Works
## Prevention
```

**Categories:** bug track — `build-errors/`, `test-failures/`, `runtime-errors/`, `performance-issues/`, `database-issues/`, `security-issues/`, `ui-bugs/`, `integration-issues/`, `logic-errors/`; knowledge track — `architecture-patterns/`, `design-patterns/`, `tooling-decisions/`, `conventions/`, `workflow-issues/`, `best-practices/`.

### 6. Grounding validation

Before anything becomes permanent knowledge, validate every NEW or UPDATED instinct and solution doc:

- **Paths:** every cited file path must exist in the current tree — or be explicitly marked historical ("removed by this fix", "pre-#NNN").
- **References:** cite PR/issue numbers, never bare commit SHAs (squash-merges rewrite SHAs and kill them).
- **Claims:** anything you can't verify against the source right now gets softened to "per this session's conclusion — …".

These are prompt-level checks — verify with quick greps/`ls`, fix what fails.

### 7. Handle lifecycle thresholds

- **Promote — ✓ ≥ 3** and the instinct passes the "What Makes a Good Instinct" bar (especially durable + surprising): move it to CLAUDE.md under the `## Proven Instincts (coach)` heading. Drop the evidence prefix on promotion and remove the line (and its index entry) from coach-lessons.md. Skip the promotion if CLAUDE.md already covers the same rule — keep the line and note it with a trailing `NOTE: … already covered by CLAUDE.md`.
- **Rewrite/remove — ✗ > ✓ AND the most recent event was a violation:** autonomously rewrite the instinct to be sharper, or remove it if it's no longer useful. (The and-clause protects instincts that were violated early but ended healthy.)
- **Dormant** (✓0 and no evidence event in 6+ months) is handled only by the sweep (step 8), never by a capture run.

### 8. Write everything — no approval

Write all changes directly, then emit a single terse summary line:

```
Coach: ✓+2 ✗+1 · 2 new · 1 promotion · 1 solution doc · skipped (unverified): 1 → <files written>
```

Write rules:
- **Instincts:** update `.claude/coach-lessons.md` in place. Append new instincts to the end of the best-fitting existing section (create a new section sparingly). **Never re-sort lines** — only the sweep sorts. For every added/removed instinct, add/remove its one-line entry in the `## Index` block; do not rebuild or reorder the rest of the index.
- **Promotions:** apply per step 7.
- **Solution doc:** `mkdir -p docs/solutions/<category>/`, write `docs/solutions/<category>/<slug>.md`.
- **`dry-run`:** print the proposed changes and stop WITHOUT writing.

**Mini-3S sweep (only when due):** if the cadence count from step 1 is **≥ 10**, run a bounded sweep after this run's writes — keep it to minutes:
- **Dedupe** near-duplicate instincts (same trigger/action): merge into one line — sum ✓/✗, keep the latest date and the clearest wording.
- **Prune** per step 7's rules; remove dormant lines (✓0, no event in 6+ months).
- **Grounding spot-check** only the sections touched this session.
- **Rebuild the index** (one line per instinct; every index line must grep back to exactly one body line) and re-sort instincts within each section by ✓ desc, then date desc (the ONLY place sorting happens).
- **Reset the cadence:** set the `<!-- coach-last-sweep: … -->` comment to the current UTC timestamp.
- Add one clause to the summary line: `· mini-3S: 2 pruned, 1 merged`.

### 9. Commit and push

- Stage changed files (coach-lessons.md, CLAUDE.md if promoted, solution doc if created)
- Commit with: `coach: capture lessons from <branch-name> session` — append ` (+sweep)` if the sweep ran
- Push to the branch's remote. Coach commits are documentation-only and should always land on the remote — an unpushed coach commit gets forgotten.

## Coach Lessons File Structure

```markdown
# Coach Lessons

> Instincts extracted from development sessions. Evidence: `[✓confirmed ✗violated · last-event]`.
> Scan this index; grep the quoted phrase for the full instinct.
<!-- coach-last-sweep: 2026-07-19T00:00:00Z -->

## Index

- [Code] <≤10-word trigger with a distinctive literal substring>
- …one line per instinct…

## Code & Architecture

- `[✓1 ✗0 · 2026-07-11]` **When** ... → **do** ... → **because** ...
```

**Index rules:** one line per instinct — `- [<short section tag>] <≤10-word trigger>`. Each index line must contain at least one distinctive **literal substring** of its body line (a flag name, token, error string) so it greps back to exactly one instinct. Section tags are bracketed short forms of the section names (`[Code]`, `[Testing]`, `[Git]`, `[DB]`, `[Deploy]`, …).

## What Makes a Good Instinct

- **Specific**: "when adding columns to an existing SQLite table" not "when using the database"
- **Actionable**: tells you exactly what to do, not just what to avoid
- **Justified**: the "because" explains the real consequence
- **Surprising**: a competent developer wouldn't already know this
- **Durable**: will still be true next month

## What Makes a Good Solution Doc

- **Non-trivial**: required real investigation, not just a config change
- **Reusable**: someone else could hit this problem
- **Complete**: includes what didn't work, not just what did
- **Searchable**: good title, tags, and module name in frontmatter
