---
name: fp-plan
description: >-
  Phase 2 of the feature-pipeline suite. Use this after /fp-explore has filed
  issues and printed the M1 stop hook — when you need to turn a set of filed
  GitHub issues into an approved implementation plan and a draft PR. Triggers on:
  "plan the fix", "create the branch and PR", "draft the implementation plan",
  "ready to plan", "fp-plan", "next step after explore", "convert issues to a
  plan", "plan phase". Reads issueNumbers from state, writes a Problem Statement,
  opens a feature branch + draft PR, spawns a HEAVIER sub-agent for the numbered
  plan, and blocks on explicit user approval before writing plan to state. Does NOT
  write any code — that is /fp-implement.
version: 3.0.0
---

# fp-plan  (Phase 2 — Plan & Draft PR)

Read issues, create branch + draft PR, get a HEAVIER plan, block until approval.
One bounded turn. Code is written by /fp-implement after this skill ends.

---

## Setup

```bash
STATE=".agents/skills/feature-pipeline/scripts/state.sh"
feature=$($STATE get feature)
issues=$($STATE get issueNumbers)   # JSON array e.g. [12,13,14]
phase=$($STATE get phase)
```

If `phase != 2` or `issueNumbers` is empty, print a clear explanation and end
the turn — running out of order produces bad state that's hard to recover from.

---

## Step 1 — Problem Statement

Read each issue body:

```bash
gh issue view <N> --json title,body
```

Write a single paragraph Problem Statement: what is broken, why it matters,
and what a correct fix should achieve. This is the anchor for the plan —
HEAVIER will produce better output when it has a crisp statement of intent.

---

## Step 2 — Create branch and draft PR

Slugify the feature name, create the branch, and push it before opening the PR
(GitHub requires the branch to exist first):

```bash
slug=$(echo "$feature" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | cut -c1-40)
branch="fix/${slug}-findings"

git checkout -b "$branch"
git push -u origin "$branch"

$STATE set branch "$branch"
```

Open a draft PR via GitHub MCP (`mcp__github__create_pull_request`):

- **title**: `fix({{feature}}): address exploration findings`
- **labels**: `draft`, `needs-plan`
- **draft**: true
- **body**:

```markdown
## Problem Statement
<from Step 1>

## Related issues
- Closes #N
- Closes #M

## Plan
_To be filled after approval._
```

Persist PR info to state so downstream skills can find it without user input:

```bash
$STATE set prNumber <N>
$STATE set prUrl    "<url>"
```

---

## Step 3 — HEAVIER plan

Spawn HEAVIER — a heavier reasoning pass gets more nuanced, file-aware plans
than the current context can produce inline. Provide:

- The issue titles and bodies
- The PR URL
- Excerpts from source files relevant to `{{feature}}`

HEAVIER brief:

> Produce a numbered implementation plan for the issues listed.
> Format each step as:
> `N. <file/area>  —  <change>  —  <rationale>  [⚠ breaking | ⚠ test-only | ⚠ schema]`
> Keep the plan to 3–8 steps. Be specific about file paths and function names.

Present the plan to the user verbatim and wait. Do not proceed until the user
explicitly types "approve", "continue", or provides edits — the whole point of
this phase is human sign-off before any code is written.

Accept inline corrections. After the user approves:

1. Update the PR body `## Plan` section with the final text.
2. Write approval to state:
   ```bash
   $STATE set planApproved true
   $STATE set phase 3
   ```
   Phase 3 signals "plan approved, ready for implement" — /fp-implement reads
   both `planApproved == true` and `phase == 3`.

Print the M2-plan stop hook and end the turn:

```
╔══ STOP HOOK M2-plan ═════════════════════════════════════════════════════════╗
║  Plan approved — branch: <branch>  PR: #<N>                                 ║
║  Run /fp-implement to commit the plan.                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Constraints

- No code changes here — /fp-implement owns that. Writing code before a plan
  is approved makes it impossible for the user to redirect without a messy
  rollback.
- Do not advance state past `phase 3` without explicit user approval.
- If HEAVIER spawning fails: write a handover to `.fp-handover.md` with the
  issue bodies and source excerpts, end the turn. Do not plan inline — the
  whole point of HEAVIER is a richer reasoning pass.
