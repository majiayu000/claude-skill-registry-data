---
name: plot-deliver
description: >-
  Verify all implementation is done, then archive the plan.
  Part of the Plot workflow. Use on /plot-deliver.
globs: []
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/skills
  version: 1.0.0-beta.1
compatibility: Designed for Claude Code and Cursor. Requires git and gh CLI.
---

# Plot: Deliver Plan

Verify all implementation is done, then archive the plan.

For docs/infra work, this is the end — live when merged. For features/bugs, `/plot-release` follows when you're ready to cut a versioned release.

**Input:** `$ARGUMENTS` is the `<slug>` of a plan on main.

Example: `/plot-deliver sse-backpressure`

## Setup

Add a `## Plot Config` section to the adopting project's `CLAUDE.md`:

    ## Plot Config
    - **Project board:** <your-project-name> (#<number>)  <!-- optional, for `gh pr edit --add-project` -->
    - **Branch prefixes:** idea/, feature/, bug/, docs/, infra/
    - **Plan directory:** docs/plans/
    - **Archive directory:** docs/archive/

### 1. Parse Input

If `$ARGUMENTS` is empty or missing:
- List active plans: `ls docs/plans/*.md 2>/dev/null`
- If exactly one exists, propose: "Found plan `<slug>`. Deliver it?"
- If multiple exist, list them and ask which one to deliver
- If none exist, explain: "No active plans found in `docs/plans/`."

Extract `slug` from `$ARGUMENTS` (trimmed, lowercase, hyphens only).

### 2. Verify Plan Exists

Check that `docs/plans/<slug>.md` exists on main.

- If not found, check `docs/archive/*-<slug>.md` — if found there: "Already delivered and archived."
- If not found anywhere: "No plan found at `docs/plans/<slug>.md`."

### 3. Read and Parse Plan

Read `docs/plans/<slug>.md` and parse the `## Branches` section for PR references.

Expected format after `/plot-approve`:
```markdown
- `feature/name` — description → #12
```

### 4. Verify All PRs Merged

Run the helper:

```bash
../plot/scripts/plot-impl-status.sh <slug>
```

Or for each PR number found in the Branches section:

```bash
gh pr view <number> --json state,isDraft --jq '{state: .state, isDraft: .isDraft}'
```

- If all are `MERGED`: proceed to step 5
- If any are `OPEN`:
  - List them and ask the user: "These PRs are still open. Merge them first, or deliver anyway?"
  - If user declines, stop and list the unfinished PRs
- If any are `CLOSED` (not merged): warn — these need manual attention

### 5. Verify Plan Completeness

Compare what the plan promised against what was actually delivered.

1. **Extract deliverables** from the plan file. Look for actionable items in sections like `## Design`, `## Branches`, or bulleted lists that describe what should be built. Number each deliverable for reference.

2. **Gather PR evidence using parallel subagents.** Launch one Task agent per merged PR to review what was implemented:
   - Each agent receives the PR number and the full list of deliverables.
   - Each agent runs `gh pr diff <number>` and reads the PR body via `gh pr view <number> --json title,body,files`.
   - Each agent returns: which deliverables (by number) are addressed by that PR, with a one-line summary of the evidence for each.
   - Launch all PR agents in parallel since they are independent.

3. **Consolidate results.** Merge the per-PR reports into a single checklist. For each deliverable, mark it:
   - **Done** — clear evidence in one or more PRs
   - **Partial** — some work done but not fully matching the plan
   - **Missing** — no evidence found in any PR

4. **Present the checklist** to the user and **ask to confirm** the plan is complete enough to deliver.
   - If all items are done: "All deliverables verified. Proceed with archive?"
   - If any are partial/missing: list them and ask "Deliver anyway, or hold off?"
   - If the user declines, stop — do not archive.

### 6. Archive Plan

```bash
git checkout main
git pull origin main
DELIVER_DATE=$(date -u +%Y-%m-%d)
git mv docs/plans/<slug>.md docs/archive/${DELIVER_DATE}-<slug>.md
git add docs/archive/${DELIVER_DATE}-<slug>.md
git commit -m "plot: deliver <slug>"
git push
```

### 7. Summary

Print:
- Delivered: `<slug>`
- Archived to: `docs/archive/<DELIVER_DATE>-<slug>.md`
- All implementation PRs: merged
- Type reminder:
  - If feature/bug: "Run `/plot-release` when ready to cut a versioned release."
  - If docs/infra: "Live on main — no release needed."
