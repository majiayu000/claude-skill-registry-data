---
name: debugging
description: >
  Use whenever working on a bug or production incident, from triage through fix through
  verification. Triggers on: "fix this bug", "there's an error", "something is broken",
  "debug this", "this isn't working", "root cause", "production issue", "the site/app is
  down", "hotfix needed", "investigate this". Covers both backlog bugs and live incidents —
  severity determines urgency and process, not two separate skills.
---

# Debugging

You are doing systematic bug investigation and resolution. The goal is not to stop the
symptom — it's to understand why it happened, fix it correctly, prevent it recurring, and
hand off cleanly. **Never fix a bug you don't understand.**

## Step 1: Classify severity

| Severity | Definition | Process |
|---|---|---|
| Critical | Production down, data loss, or security exposure | Incident mode (below). Investigate within 2 hours, fix or workaround within 24. |
| High | Major feature broken, no workaround | Fix in current session/sprint. No unrelated work until resolved. |
| Medium | Degraded behavior, workaround exists | Normal backlog priority. |
| Low | Cosmetic or edge-case | Batch with related work. |

**Critical only — Incident mode:**
1. State the severity and what's affected, in one sentence, before doing anything else.
2. Mitigate first, root-cause second: rollback, disable the feature flag, or scale up — restore
   service before you fully understand why it broke, if a known-safe mitigation exists.
3. Once mitigated, continue with root cause below at normal urgency.
4. Write a post-mortem (template at the bottom) for any Critical or High severity issue.

## Step 2: Reproduce first

Before writing a single character of fix code:
1. Read the report completely — expected vs. actual behavior.
2. Reproduce it yourself. Document your reproduction steps (they may differ from the report).
3. If you cannot reproduce: try alternate paths (different data, different order, timing),
   check for intermittency, and say so explicitly rather than guessing at a fix.

## Step 3: Root cause — 5 Whys

Do not skip this. A fix without root cause is a patch that creates the next bug.

```
Why 1: Why did the bug occur?          → [symptom]
Why 2: Why did [symptom] happen?       → [closer to root]
Why 3: Why did [that] happen?          → [closer still]
Why 4: Why did [that] happen?          → [closer still]
Why 5: Why did [that] happen?          → [actionable root cause]
```

Stop when you reach something you can actually act on (a missing check, a wrong assumption,
a race condition) — not before, not after.

## Step 4: Fix with a regression test

**Every bug fix requires a test that fails before the fix and passes after.** "Fixed without a
test" is not an accepted resolution. If this project uses `unlazy` gates (it does, via `sdlc` —
see `docs/sdlc/<slug>/` if this bug traces to an existing slug), express the regression test as
a gate: `CHECK:` runs the reproduction, `EXPECT:` matches only the fixed behavior. Confirm the
gate fails on the pre-fix code before you start fixing — a check that can't fail is worthless.

## Step 5: Close the loop

If the fix reveals follow-up work (a related bug, a needed refactor, a missing safeguard) that
is out of scope for this fix, don't silently drop it — write a new `intent.md` for it via the
`sdlc` skill's intent interview, so it re-enters the backlog instead of being forgotten. This
is how "maintain" feeds back into "plan" without a human having to remember to file it.

## Post-Mortem Template (Critical/High only)

```
Incident: [one-line description]
Date/Duration: [start–end]
Severity: [Critical | High]

Timeline: [chronological events]
Root Cause: [from the 5 Whys above]
Contributing Factors: [what made this worse or harder to detect]
Impact: [what broke, for how long, who/what was affected]
What prevents recurrence: [test added / process change / code change]
Follow-up intent.md filed: [slug, or "none needed"]
```
