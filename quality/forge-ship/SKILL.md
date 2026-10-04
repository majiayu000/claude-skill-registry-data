---
name: forge-ship
description: Phase 4 of the Forge pipeline. Summarize the whole workload — what was built, which Beads issues closed, a before/after, and a step-by-step walkthrough the user can run to verify it themselves — then run quality gates, push, and open the PR. Use when starting /forge-ship or the ship step of /forgemaster.
---

# forge-ship

Phase 4 of 4 in the Forge pipeline (research → plan → implement → **ship**). It closes the loop: a
human-readable summary of the entire run plus the actual push/PR. Output is `reports/<slug>-ship.md`
and a pushed branch with a PR.

This phase complements the existing [[ship]] command — it adds the **narrative summary and test
walkthrough** on top of the quality-gate/commit/push mechanics.

## When to Use

- The user runs `/forge-ship <slug>` or `/forgemaster` enters its ship phase.
- The implement phase is complete (all checkpoints demoed, tasks closed).

## Prerequisites

```bash
bun run forge:phase-gate ship --slug <slug>     # verifies implement is complete in forge state
cat plans/research/<slug>.md                    # original goal
cat plans/drafts/<slug>.md                      # plan + checkpoints + Beads map
```

Beads must be reachable. If `bd` errors, stop and fix it (`bd dolt start`) before shipping.

## Process

### 1. Gather the facts

```bash
git log --oneline <base>..HEAD          # commits this run produced
git diff --stat <base>..HEAD            # files + churn
bd list --json                          # to confirm which planned tasks are closed
```

Cross-reference against the plan's Beads Issue Map so every planned task is accounted for
(closed, or explicitly deferred with a reason).

### 2. Build the before/after

Describe the observable change, not the diff. For each checkpoint: what the user could NOT do
before, and what they can do now. Capture commands/URLs and expected output.

### 3. Write the ship report

Write to `reports/<slug>-ship.md` (create `reports/` if needed):

```markdown
# Ship Report: <slug> — <feature title>
Shipped: <date>
Epic/Feature: <beads id> · Branch: <branch> · PR: <url once created>

## What Shipped
<2–4 sentences: the capability delivered, in plain language>

## Before → After
| Area | Before | After |
|------|--------|-------|
| <capability> | <old behavior / "did not exist"> | <new behavior> |

## Work Done
- Checkpoint A — <summary> (<commit shas>)
- Checkpoint B — <summary> (<commit shas>)

## Beads Completed
| Beads ID | Title | Status |
|----------|-------|--------|
| <id> | <title> | closed |

## Test It Yourself (walkthrough)
1. <setup step, e.g. `bun install` / `bun run dev`>
2. <action — exact command or UI steps>
   - Expect: <observable result>
3. Automated: `bun test <paths>` — expect all green.

## Follow-ups / Known Gaps
- <deferred Beads id + reason, or "none">
```

### 4. Quality gates, push, PR

Run the standard ship mechanics (reuse [[ship]] for detail):

```bash
bun run typecheck && bun run lint && bun test
git status --porcelain                 # must be empty
git pull --rebase origin <base>
git push origin <branch>
```

The PR body MUST follow the canonical template — see [[pr-description]]. The ship report you just
wrote is the source material: map its sections into the template (What Shipped → What Changed, the
goal from research → Why It's Needed, the **Test It Yourself** walkthrough → How It Was Tested, real
gate output → Test Evidence) and fill Risk & Rollback + Linked Issues & AC Trace.

```bash
mkdir -p .tmp/work
cp .claude/skills/pr-description/references/pr-template.md .tmp/work/pr-body.md
# Fill every section from reports/<slug>-ship.md + the plan's Beads map, then validate:
bun run .claude/skills/pr-description/scripts/check-pr-body.ts .tmp/work/pr-body.md   # must be "ok": true

gh pr create --title "<feature title>" --base <base> --body "$(cat .tmp/work/pr-body.md)"
```

Keep `reports/<slug>-ship.md` as the durable in-repo record; the PR body is the template-conformant
view of the same run.

### 5. Close out Beads + state

```bash
bd close <epic-or-feature-id>
bd comments add <epic-or-feature-id> "worklog: shipped — PR #<n>; report reports/<slug>-ship.md"
bd dolt push
bun run forge:phase-gate ship --slug <slug> --write     # records the run complete
```

After ship completes, the forge run is finished — the Stop hook goes quiet and the state file can
be archived or removed.

### 6. Present to the user

```
🚀 Shipped: <slug>
Report: reports/<slug>-ship.md
PR: <url>
Beads closed: <ids>

Try it: <the single most representative command from the walkthrough>
```

## Exit Criteria

- [ ] `reports/<slug>-ship.md` exists with before/after, Beads table, and a runnable walkthrough.
- [ ] Quality gates pass; branch pushed; PR created with a [[pr-description]]-conformant body
      (`check-pr-body.ts` reports `ok: true`).
- [ ] Every planned Beads task is closed or deferred-with-reason; epic/feature closed.
- [ ] Forge state advanced to `ship` complete.
