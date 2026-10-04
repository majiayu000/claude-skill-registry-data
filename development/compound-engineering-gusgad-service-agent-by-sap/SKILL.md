---
name: compound-engineering
description: Use after solving a non-trivial bug or making a non-obvious decision, to capture it as durable, searchable documentation so the next session doesn't re-derive it from scratch - and use at the start of related work to check whether that documentation already exists.
---

# Compound Engineering

## Overview

**Core idea:** each unit of engineering work should make the next unit easier, not just add to the pile. The first time a problem is solved, it costs real investigation. Documented well, the second occurrence costs minutes. Undocumented, it costs the same investigation again — and again, across however many sessions hit it.

This is the same principle behind a growing test suite or a growing set of lint rules, applied to *knowledge* instead of code: a session's hard-won context (why this bug happened, why this approach was chosen over that one, what didn't work) either evaporates when the session ends, or gets written down where the next session — human or agent — can find it before repeating the work.

## The Loop

1. **Plan** — before writing code, understand the problem and check whether it's already been solved (see Grounding First, below)
2. **Work** — implement with tests (see the `test-driven-development` skill under `superpowers/`)
3. **Assess** — review the change for correctness and quality (see the `code-review` skill)
4. **Compound** — capture what was learned somewhere durable, so the next pass through this loop starts further ahead

Step 4 is the one that's easy to skip because the task already feels done once tests pass. It's also the one that makes the next task faster — skipping it is why the same class of bug gets independently re-investigated by every session that hits it.

## Grounding First

Before investigating a bug or non-obvious problem from scratch, check whether it's already documented:

```bash
grep -ril "<keyword>" docs/solutions/ 2>/dev/null
```

If `docs/solutions/` doesn't exist yet in this repo, that's fine — it means nothing has been captured yet, not that nothing is worth capturing. Create it with the first entry.

## What's Worth Capturing

**Capture when:**
- The root cause wasn't obvious and took real investigation (see `systematic-debugging` under `superpowers/`)
- A decision was made between multiple viable approaches, for reasons that won't be obvious from the code alone (why Sequelize migration X handles tenant scoping this way, why the Kafka consumer retries the way it does)
- The fix would plausibly recur elsewhere in the codebase (a pattern, not a one-off typo)

**Don't capture:**
- Trivial fixes (typos, obvious off-by-ones) — the git history already documents these adequately
- In-progress or unverified work — only document a solution once it's actually confirmed working (see `verification-before-completion`)
- Anything that duplicates what the code or its tests already make clear

## How to Capture It

Write one markdown file per learning to `docs/solutions/<category>/<short-slug>.md`. Categories: something like `build-errors/`, `runtime-errors/`, `database-issues/`, `architecture-decisions/`, `conventions/` — pick or create whatever fits, keep it a flat, browsable structure rather than deep nesting.

Minimal shape:

```markdown
---
title: <short, searchable title>
date: YYYY-MM-DD
tags: [component, error-type]
---

## Problem
1-2 sentences: what broke, or what question needed an answer.

## What Didn't Work
(if applicable) Approaches tried and ruled out, and why — this is often
the most valuable part, since it prevents someone else re-trying the
same dead end.

## Root Cause / Decision
The actual explanation, or the reasoning behind the choice made.

## Solution
The fix or the approach taken, with a code reference (`file:line`) rather
than a pasted snippet that can drift out of sync with the code.

## Prevention
How to avoid this recurring, if applicable — a test added, a convention
to follow, a check to run.
```

Before asserting how code behaves in the writeup, read the actual current source — don't document from memory of how the conversation went. A claim that isn't grounded in the current tree is how a knowledge base accumulates stale, misleading entries.

**One learning per file, one file per run.** Don't batch several unrelated learnings into one entry — that makes it un-findable later and harder to keep accurate as the codebase moves on.

## Keeping It Findable

The knowledge only compounds if the next session actually knows to look. If this repo's root instructions file (e.g. `CLAUDE.md` or `AGENTS.md`, if one exists) doesn't already mention `docs/solutions/`, add a short line pointing at it once the directory exists — not a whole section, just enough that a fresh session knows the directory is there and roughly what it's organized by.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Documenting mid-investigation, before the fix is verified | Wait until `verification-before-completion` has actually passed |
| Writing from memory of the conversation instead of the current code | Read the defining source line before asserting behavior in the writeup |
| One giant file accumulating every learning | One file per learning, organized into categories |
| Creating a new doc when an existing one already covers this problem | Search `docs/solutions/` first; update the existing doc instead of duplicating |
| Capturing everything, including trivial fixes | Reserve it for non-obvious root causes and durable decisions — git history covers the rest |
